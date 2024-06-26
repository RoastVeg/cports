pkgname = "openssh"
# XXX the version here is a workaround to force an upgrade, fix it next bump
pkgver = "9.7.1_p1"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--datadir=/usr/share/openssh",
    "--sysconfdir=/etc/ssh",
    "--disable-wtmp",
    "--disable-utmp",
    "--without-selinux",
    "--without-rpath",
    "--without-zlib-version-check",
    "--with-mantype=doc",
    "--with-pam",
    "--with-libedit",
    "--with-pid-dir=/run",
    "--with-privsep-user=nobody",
    "--with-privsep-path=/var/chroot/ssh",
    "--with-xauth=/usr/bin/xauth",
    "--with-security-key-builtin",
    "--with-ssl-engine",
    "--disable-strip",
    "ac_cv_header_sys_cdefs_h=false",
]
make_check_target = "tests"
make_check_args = ["-j1"]
hostmakedepends = [
    "automake",
    "pkgconf",
]
makedepends = [
    "libedit-devel",
    "libfido2-devel",
    "libldns-devel",
    "linux-pam-devel",
    "openssl-devel",
    "zlib-devel",
]
pkgdesc = "OpenSSH free Secure Shell (SSH) client and server implementation"
maintainer = "q66 <q66@chimera-linux.org>"
license = "SSH-OpenSSH"
url = "https://www.openssh.com"
# source = f"https://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/{pkgname}-{pkgver.replace('_', '')}.tar.gz"
source = (
    "https://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-9.7p1.tar.gz"
)
sha256 = "490426f766d82a2763fcacd8d83ea3d70798750c7bd2aff2e57dc5660f773ffd"
file_modes = {"usr/libexec/ssh-keysign": ("root", "root", 0o4755)}
# FIXME cfi (does not work); maybe make testsuite work first
hardening = ["vis", "!cfi"]
# portable openssh is not very portable
options = ["!check"]


def init_configure(self):
    self.configure_args += [
        "--with-ldns=" + str(self.profile().sysroot / "usr")
    ]


def post_install(self):
    self.install_license("LICENCE")

    self.install_file(
        self.files_path / "sshd.pam", "usr/lib/pam.d", name="sshd"
    )

    self.install_bin("contrib/ssh-copy-id")
    self.install_man("contrib/ssh-copy-id.1")

    self.install_dir("var/chroot/ssh", empty=True)

    self.install_dir("etc/ssh/ssh_config.d", empty=True)
    self.install_dir("etc/ssh/sshd_config.d", empty=True)

    self.install_service(self.files_path / "ssh-keygen")
    self.install_service(self.files_path / "sshd")
