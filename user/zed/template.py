pkgname = "zed"
pkgver = "0.139.3"
pkgrel = 0
# no upstream support for others
archs = ["x86_64"]
build_style = "cargo"
hostmakedepends = ["cargo-auditable", "pkgconf", "protoc"]
makedepends = [
    "alsa-lib-devel",
    "fontconfig-devel",
    "libgit2-devel",
    "libxcb-devel",
    "libxkbcommon-devel",
    "vulkan-headers",
    "vulkan-loader-devel",
    "wayland-devel",
    "zstd-devel"
]
pkgdesc = "High-performance, multiplayer code editor"
maintainer = "roastveg <louis@hamptonsoftworks.com>"
license = "AGPL-3.0-or-later AND Apache-2.0 AND GPL-3.0-or-later"
url = "https://zed.dev"
source = f"https://github.com/zed-industries/zed/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "cd15f80c95ec4c33cbe821ff70e64c3922d1187fa13ac894a8049b615cad2e4f"
env = {
    "RUSTFLAGS": "-Clink-args=-Wl,-z,nostart-stop-gc",
    "ZED_UPDATE_EXPLANATION": "Updates are managed by Chimera",
}
# tests require vulkan
options = ["!check"]


def post_extract(self):
    # overrides the linker to mold
    self.rm(".cargo/config.toml")


def post_build(self):
    self.cargo.build(args=["-p", "zed", "-p", "cli"])


def do_install(self):
    self.install_license("LICENSE-AGPL")
    self.install_license("LICENSE-APACHE")
    self.install_license("LICENSE-GPL")
    self.install_bin(f"target/{self.profile().triplet}/release/cli", name="zeditor")
    self.install_file(
        f"target/{self.profile().triplet}/release/zed",
        "usr/libexec/zed-editor",
        0o755,
    )
    self.install_file(
        f"crates/zed/resources/app-icon.png",
        "usr/share/icons/hicolor/512x512/apps",
        name="zed.png"
    )
    self.install_file(
        f"crates/zed/resources/app-icon@2x.png",
        "usr/share/icons/hicolor/1024x1024/apps",
        name="zed.png"
    )
    self.install_file(
        self.files_path / "zed.desktop", "usr/share/applications"
    )
