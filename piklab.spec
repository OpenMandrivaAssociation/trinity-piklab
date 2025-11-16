#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg piklab
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.15.2
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	IDE for PIC-microcontroller development [Trinity]
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/development/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:	cmake make
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

# READLINE support
BuildRequires:	pkgconfig(readline)

# LIBUSB support
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libusb)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
Piklab is an integrated development environment for applications based on
Microchip PIC and dsPIC microcontrollers similar to the MPLAB environment.

Support for several compiler and assembler toolchains is integrated. The
GPSim simulator, the ICD1 programmer, the ICD2 debugger, the PICkit1 and
PICkit2 programmers, the PicStart+ programmer, and most direct programmers
are supported. A command-line programmer and debugger are also available.


##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########


%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INSTALL_PREFIX=%{tde_prefix} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DDATA_INSTALL_DIR=%{tde_datadir}/apps \
  -DMIME_INSTALL_DIR=%{tde_datadir}/mimelnk \
  -DXDG_APPS_INSTALL_DIR=%{tde_tdeappdir} \
  -DSHARE_INSTALL_PREFIX="%{tde_datadir}"\
  -DDOC_INSTALL_DIR=%{tde_tdedocdir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  \
  -DBUILD_ALL=ON \
  -DWITH_ALL_OPTIONS=ON \
  ..

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot} -C build

%find_lang %{tde_pkg}


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_bindir}/piklab
%{tde_bindir}/piklab-coff
%{tde_bindir}/piklab-hex
%{tde_bindir}/piklab-prog
%{tde_tdeappdir}/piklab.desktop
%{tde_datadir}/apps/katepart/syntax/asm-pic.xml
%{tde_datadir}/apps/katepart/syntax/coff-c-pic.xml
%{tde_datadir}/apps/katepart/syntax/coff-pic.xml
%{tde_datadir}/apps/katepart/syntax/jal-pic.xml
%{tde_datadir}/apps/piklab
%{tde_tdedocdir}/HTML/en/piklab
%{tde_datadir}/icons/hicolor/*/*/*.png
%{tde_datadir}/mimelnk/application/x-piklab.desktop
%{tde_mandir}/man1/piklab-coff.1
%{tde_mandir}/man1/piklab-hex.1
%{tde_mandir}/man1/piklab-prog.1
%{tde_mandir}/man1/piklab.1

