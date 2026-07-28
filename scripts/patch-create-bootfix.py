#!/usr/bin/env python3
"""Patch Create 6.0.10 AllAdvancements to avoid chocolate_bucket boot crash.

Create eagerly resolves fluid bucket icons during TRIGGER_TYPES RegisterEvent.
On large modpacks that can hit unbound DeferredHolders (create:chocolate_bucket).
See https://github.com/Creators-of-Create/Create/pull/10534

This rewrites FluidEntry.get().getBucket() icon sources to Items.COCOA_BEANS.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

ASM_VERSION = "9.7"
ASM_JARS = {
    "asm": f"https://repo1.maven.org/maven2/org/ow2/asm/asm/{ASM_VERSION}/asm-{ASM_VERSION}.jar",
    "asm-tree": f"https://repo1.maven.org/maven2/org/ow2/asm/asm-tree/{ASM_VERSION}/asm-tree-{ASM_VERSION}.jar",
    "asm-commons": f"https://repo1.maven.org/maven2/org/ow2/asm/asm-commons/{ASM_VERSION}/asm-commons-{ASM_VERSION}.jar",
}

PATCHER_JAVA = r"""
import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.jar.*;

public class PatchCreateAdvancements {
  static final String AA = "com/simibubi/create/foundation/advancement/AllAdvancements";
  static final String BUILDER = "com/simibubi/create/foundation/advancement/CreateAdvancement$Builder";
  static final String FLUID_ENTRY = "com/tterrag/registrate/util/entry/FluidEntry";
  static final String FLOWING = "net/neoforged/neoforge/fluids/BaseFlowingFluid$Flowing";
  static final String ITEM = "net/minecraft/world/item/Item";
  static final String ITEM_LIKE = "net/minecraft/world/level/ItemLike";

  public static void main(String[] args) throws Exception {
    Path in = Path.of(args[0]);
    Path out = Path.of(args[1]);
    byte[] original;
    try (JarFile jar = new JarFile(in.toFile())) {
      JarEntry e = jar.getJarEntry(AA + ".class");
      if (e == null) throw new IllegalStateException("AllAdvancements missing");
      original = jar.getInputStream(e).readAllBytes();
    }

    ClassNode cn = new ClassNode();
    new ClassReader(original).accept(cn, 0);

    int patched = 0;
    for (MethodNode mn : cn.methods) {
      if (!mn.name.startsWith("lambda$static$")) continue;
      if (patchFluidBucketIcon(mn)) {
        patched++;
        System.out.println("patched " + mn.name);
      }
    }
    if (patched == 0) {
      // Already patched or unexpected Create version — copy through.
      System.out.println("No fluid-bucket icon lambdas found; copying jar unchanged");
      Files.copy(in, out, StandardCopyOption.REPLACE_EXISTING);
      return;
    }

    ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
    cn.accept(cw);
    byte[] rewritten = cw.toByteArray();

    if (out.getParent() != null) Files.createDirectories(out.getParent());
    try (JarFile inJar = new JarFile(in.toFile());
         JarOutputStream jos = new JarOutputStream(Files.newOutputStream(out))) {
      Enumeration<JarEntry> en = inJar.entries();
      byte[] buf = new byte[8192];
      while (en.hasMoreElements()) {
        JarEntry e = en.nextElement();
        String name = e.getName();
        if (name.equals(AA + ".class")) {
          jos.putNextEntry(new JarEntry(name));
          jos.write(rewritten);
          jos.closeEntry();
          continue;
        }
        if (name.startsWith("META-INF/") &&
            (name.endsWith(".SF") || name.endsWith(".RSA") || name.endsWith(".DSA") || name.endsWith(".EC"))) {
          continue;
        }
        jos.putNextEntry(new JarEntry(name));
        if (!e.isDirectory()) {
          try (InputStream is = inJar.getInputStream(e)) {
            int n;
            while ((n = is.read(buf)) > 0) jos.write(buf, 0, n);
          }
        }
        jos.closeEntry();
      }
    }
    System.out.println("Wrote " + out + " (" + patched + " lambdas patched)");
  }

  static AbstractInsnNode nextInsn(AbstractInsnNode n) {
    while (n != null) {
      n = n.getNext();
      if (n == null) return null;
      int op = n.getOpcode();
      if (op >= 0) return n; // skip labels / frames / line numbers
    }
    return null;
  }

  static boolean patchFluidBucketIcon(MethodNode mn) {
    InsnList insns = mn.instructions;
    for (AbstractInsnNode a = insns.getFirst(); a != null; a = a.getNext()) {
      if (!(a instanceof FieldInsnNode fa) || fa.getOpcode() != Opcodes.GETSTATIC) continue;
      if (!fa.owner.equals("com/simibubi/create/AllFluids")) continue;
      AbstractInsnNode b = nextInsn(a);
      AbstractInsnNode c = nextInsn(b);
      AbstractInsnNode d = nextInsn(c);
      AbstractInsnNode e = nextInsn(d);
      if (!(b instanceof MethodInsnNode mb) || mb.getOpcode() != Opcodes.INVOKEVIRTUAL) continue;
      if (!mb.owner.equals(FLUID_ENTRY) || !mb.name.equals("get")) continue;
      if (!(c instanceof TypeInsnNode tc) || tc.getOpcode() != Opcodes.CHECKCAST) continue;
      if (!tc.desc.equals(FLOWING)) continue;
      if (!(d instanceof MethodInsnNode md) || md.getOpcode() != Opcodes.INVOKEVIRTUAL) continue;
      if (!md.owner.equals(FLOWING) || !md.name.equals("getBucket")) continue;
      if (!(e instanceof MethodInsnNode me) || me.getOpcode() != Opcodes.INVOKEVIRTUAL) continue;
      if (!me.owner.equals(BUILDER) || !me.name.equals("icon")) continue;
      if (!me.desc.equals("(L" + ITEM_LIKE + ";)L" + BUILDER + ";")) continue;

      InsnList rep = new InsnList();
      rep.add(new FieldInsnNode(Opcodes.GETSTATIC,
          "net/minecraft/world/item/Items", "COCOA_BEANS", "L" + ITEM + ";"));
      insns.insertBefore(a, rep);
      insns.remove(a);
      insns.remove(b);
      insns.remove(c);
      insns.remove(d);
      return true;
    }
    return false;
  }
}
"""


def ensure_asm(cache: Path) -> list[Path]:
    cache.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, url in ASM_JARS.items():
        dest = cache / f"{name}-{ASM_VERSION}.jar"
        if not dest.exists():
            print(f"download {dest.name}")
            urllib.request.urlretrieve(url, dest)
        paths.append(dest)
    return paths


def patch_jar(src: Path, dst: Path, work: Path) -> None:
    java = shutil.which("java")
    javac = shutil.which("javac")
    if not java or not javac:
        # Prefer Homebrew OpenJDK on macOS
        for root in ("/opt/homebrew/opt/openjdk/bin", "/usr/local/opt/openjdk/bin"):
            if (Path(root) / "java").exists():
                java = str(Path(root) / "java")
                javac = str(Path(root) / "javac")
                break
    if not java or not javac:
        raise SystemExit("java/javac required to patch Create")

    asm = ensure_asm(work / "asm")
    cp = ":".join(str(p) for p in asm)
    src_java = work / "PatchCreateAdvancements.java"
    src_java.write_text(PATCHER_JAVA, encoding="utf-8")
    import subprocess

    subprocess.check_call([javac, "-cp", cp, str(src_java)], cwd=work)
    tmp_out = work / "create-patched.jar"
    subprocess.check_call(
        [java, "-cp", f"{work}:{cp}", "PatchCreateAdvancements", str(src), str(tmp_out)],
        cwd=work,
    )
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(tmp_out), str(dst))


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input-create.jar> <output-create.jar>")
        raise SystemExit(2)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    if not src.is_file():
        raise SystemExit(f"missing {src}")

    # Idempotent: if already patched (no getBucket in AllAdvancements), copy.
    with zipfile.ZipFile(src) as z:
        data = z.read("com/simibubi/create/foundation/advancement/AllAdvancements.class")
    if b"getBucket" not in data and b"COCOA_BEANS" in data:
        print("already patched; copying")
        shutil.copy2(src, dst)
        return

    with tempfile.TemporaryDirectory(prefix="create-bootfix-") as tmp:
        patch_jar(src, dst, Path(tmp))


if __name__ == "__main__":
    main()
