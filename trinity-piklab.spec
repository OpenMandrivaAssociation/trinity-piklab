%bcond clang 1

# TDE variables
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg piklab
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Version:	0.15.2
Release:	%{?tde_version:%{tde_version}_}3
Summary:	IDE for PIC-microcontroller development [Trinity]
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/development/%{tarball_name}-%{tde_version}.tar.xz

BuildSystem:  	cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DDATA_INSTALL_DIR=%{tde_prefix}/share/apps
BuildOption:    -DMIME_INSTALL_DIR=%{tde_prefix}/share/mimelnk
BuildOption:    -DXDG_APPS_INSTALL_DIR=%{tde_prefix}/share/applications/tde
BuildOption:    -DSHARE_INSTALL_PREFIX="%{tde_prefix}/share"
BuildOption:    -DDOC_INSTALL_DIR=%{tde_prefix}/share/doc/tde
BuildOption:    -DBUILD_ALL=ON -DWITH_ALL_OPTIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}


BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:  trinity-tde-cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	fdupes

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


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"

%install -a
%find_lang %{tde_pkg}


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_prefix}/bin/piklab
%{tde_prefix}/bin/piklab-coff
%{tde_prefix}/bin/piklab-hex
%{tde_prefix}/bin/piklab-prog
%{tde_prefix}/share/applications/tde/piklab.desktop
%{tde_prefix}/share/apps/katepart/syntax/asm-pic.xml
%{tde_prefix}/share/apps/katepart/syntax/coff-c-pic.xml
%{tde_prefix}/share/apps/katepart/syntax/coff-pic.xml
%{tde_prefix}/share/apps/katepart/syntax/jal-pic.xml
%{tde_prefix}/share/apps/piklab
%{tde_prefix}/share/doc/tde/HTML/en/piklab
%{tde_prefix}/share/icons/hicolor/*/*/*.png
%{tde_prefix}/share/mimelnk/application/x-piklab.desktop
%{tde_prefix}/share/man/man1/piklab-coff.1
%{tde_prefix}/share/man/man1/piklab-hex.1
%{tde_prefix}/share/man/man1/piklab-prog.1
%{tde_prefix}/share/man/man1/piklab.1

