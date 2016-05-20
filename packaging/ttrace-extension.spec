Name:		ttrace-extension
Summary:    T-trace extension package
Version:	1.0.0
Release:    1
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: pkgconfig(capi-base-common)

%define keepstatic 1

%define TTRACE_PROFILE none
%if "%{?tizen_profile_name}" == "mobile"
%define TTRACE_PROFILE mobile
%else
%if "%{?tizen_profile_name}" == "tv"
%define TTRACE_PROFILE tv
%else
%if "%{?tizen_profile_name}" == "wearable"
%define TTRACE_PROFILE wearable
%endif
%endif
%endif

%define TTRACE_TIZEN_VERSION_MAJOR 2
%if "%{?tizen_version_major}" == "3"
%define TTRACE_TIZEN_VERSION_MAJOR 3
%endif

%description
T-trace extension library

%package devel
Summary:    T-trace extension for tizen
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
T-trace extension library devel

%prep
%setup -q

%build
export CFLAGS="$CFLAGS -g -Wall -std=gnu99"
export CXXFLAGS="$CXXFLAGS -std=c++0x -fPIE -pie"
%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIBDIR=%{_libdir} -DINCLUDEDIR=%{_includedir} \
      -DTTRACE_PROFILE=%{TTRACE_PROFILE} -DTTRACE_TIZEN_VERSION_MAJOR=%{TTRACE_TIZEN_VERSION_MAJOR}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}/usr/share/license
cp LICENSE %{buildroot}/usr/share/license/%{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest ttrace-extension.manifest
%defattr(-,root,root,-)
%{_libdir}/libttrace-extension.so.*
/usr/share/license/%{name}

%files devel
%defattr(-,root,root,-)
%{_includedir}/ttrace-extension.h
%{_libdir}/libttrace-extension.so
%{_libdir}/libttrace-extension.a
%{_libdir}/pkgconfig/ttrace-extension.pc
%{_libdir}/pkgconfig/ttrace-extension-static.pc

