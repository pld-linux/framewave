#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Framewave - set of popular image and signal processing routines
Summary(pl.UTF-8):	Framewave - zestaw popularnych funkcji do przetwarzania obrazu i sygnału
Name:		framewave
Version:	1.3.1
Release:	9
License:	Apache v2.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/framewave/FRAMEWAVE_%{version}_SRC.tar.gz
# Source0-md5:	86a28ebfbfd70be06ab54d0d8b17ebd7
Patch0:		%{name}-system-boost.patch
Patch1:		%{name}-c++.patch
Patch2:		no-forced-arch-bits.patch
URL:		http://framewave.sourceforge.net/
BuildRequires:	boost-devel >= 1.34
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.385
BuildRequires:	scons
BuildRequires:	sed >= 4.0
ExclusiveArch:	%{ix86} %{x8664} x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Framewave(TM) is a collection of low-level software routines for x86
processors. Framewave (FW) is designed to aid and accelerate
application development, debugging, and optimization. Framewave
function capabilities extend from simple arithmetic operations to
rich, complex domain specific tasks, such as image, video, and signal
processing.

%description -l pl.UTF-8
Framewave(TM) to zestaw niskopoziomowych procedur dla procesorów x86.
Biblioteki zostały zaprojektowane tak, aby wspomóc i przyspieszyć
tworzenie aplikacji, diagnostykę i optymalizację. Możliwości funkcji
Framewave obejmują obszar od prostych operacji arytmetycznych po
złożone zadania specyficzne dla dziedziny, takie jak przetwarzanie
obrazu statycznego i ruchomego oraz sygnału.

%package devel
Summary:	Header files for Framewave libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Framewave
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Framewave libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Framewave.

%package static
Summary:	Static Framewave libraries
Summary(pl.UTF-8):	Statyczne biblioteki Framewave
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Framewave libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Framewave.

%prep
%setup -q -n FRAMEWAVE_%{version}_SRC
%patch0 -p1
%patch1 -p1
%patch2 -p1

# kill precompiled binaries
%{__rm} BuildTools/bin/FwHeaderConvert_*

%{__sed} -i -e "s/'-O2'/'%{rpmcxxflags}'/" BuildTools/buildscripts/fwflags_gcc.py

%build
cd Framewave
mkdir -p build/{include,tmp,bin}
for kind in shared %{?with_static_libs:static} ; do
%scons \
%ifarch %{x8664} x32
	bitness=64 \
%else
	bitness=32 \
%endif
	libtype=$kind \
	variant=release
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

cp -p Framewave/build/include/*.h $RPM_BUILD_ROOT%{_includedir}
install Framewave/build/bin/release_shared_*/lib*.so.*.*.* $RPM_BUILD_ROOT%{_libdir}
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
for f in $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*.* ; do
	ln -sf $(basename $f) $(echo $f | sed -e 's/[.0-9]*$//')
done
%if %{with static_libs}
install Framewave/build/bin/release_static_*/lib*.a $RPM_BUILD_ROOT%{_libdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc License.txt README
%attr(755,root,root) %{_libdir}/libfwBase.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfwBase.so.1
%attr(755,root,root) %{_libdir}/libfwImage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfwImage.so.1
%attr(755,root,root) %{_libdir}/libfwJPEG.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfwJPEG.so.1
%attr(755,root,root) %{_libdir}/libfwSignal.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfwSignal.so.1
%attr(755,root,root) %{_libdir}/libfwVideo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfwVideo.so.1

%files devel
%defattr(644,root,root,755)
%doc Framewave/doc/*.h
%attr(755,root,root) %{_libdir}/libfwBase.so
%attr(755,root,root) %{_libdir}/libfwImage.so
%attr(755,root,root) %{_libdir}/libfwJPEG.so
%attr(755,root,root) %{_libdir}/libfwSignal.so
%attr(755,root,root) %{_libdir}/libfwVideo.so
%{_includedir}/fwBase.h
%{_includedir}/fwImage.h
%{_includedir}/fwImage_sol.h
%{_includedir}/fwJPEG.h
%{_includedir}/fwSignal.h
%{_includedir}/fwVideo.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfwBase.a
%{_libdir}/libfwImage.a
%{_libdir}/libfwJPEG.a
%{_libdir}/libfwSignal.a
%{_libdir}/libfwVideo.a
%endif
