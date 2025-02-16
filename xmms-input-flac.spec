#
# Conditional build:
%bcond_with	sse2		# SSE2 instructions

%ifarch %{x8664} x32 pentium4
%define	with_sse2	1
%endif
Summary:	Free Lossless Audio Codec - XMMS plugin
Summary(pl.UTF-8):	Wtyczka FLAC dla XMMS
Name:		xmms-input-flac
# last version containing xmms plugin
Version:	1.4.1
Release:	2
License:	GPL v2+
Group:		Libraries
Source0:	https://downloads.xiph.org/releases/flac/flac-%{version}.tar.xz
# Source0-md5:	835c44ca77c4674b9cdc5b24571306ce
Patch0:		flac-xmms-only.patch
Patch1:		includes.patch
URL:		https://xiph.org/flac/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.11
BuildRequires:	doxygen
BuildRequires:	flac-devel >= 1.4.1
# for AM_ICONV
BuildRequires:	gettext-tools
BuildRequires:	libogg-devel >= 2:1.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	rpmbuild(macros) >= 1.125
BuildRequires:	tar >= 1:1.22
BuildRequires:	xmms-devel >= 0.9.5.1
BuildRequires:	xz
Requires:	flac >= 1.4.1
Requires:	xmms >= 0.9.5.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FLAC input plugin for XMMS.

%description -l pl.UTF-8
Wtyczka dla XMMS umożliwiająca odtwarzanie plików w formacie FLAC.

%prep
%setup -q -n flac-%{version}
%patch -P0 -p1
%patch -P1 -p1

%{__rm} m4/ogg.m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-examples \
	--disable-silent-rules \
	%{!?with_sse2:--disable-sse}

# force using system FLAC headers
%{__rm} -r include/FLAC*

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{xmms_input_plugindir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md COPYING.Xiph README.md
%attr(755,root,root) %{xmms_input_plugindir}/libxmms-flac.so
