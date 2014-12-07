%define debug_package %{nil}
%define _with_gcj_support 1

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

Summary:        Utility classes for concurrent Java programming
Name:           concurrent
Epoch:          0
Version:        1.3.4
Release:        15
License:        Public Domain
Url:            http://gee.cs.oswego.edu/dl/classes/EDU/oswego/cs/dl/util/concurrent/intro.html
Group:          Development/Java
Source0:        http://gee.cs.oswego.edu/dl/classes/EDU/oswego/cs/dl/current/concurrent.tar.gz
Source1:        %{name}-%{version}.build.xml
Patch0:         concurrent-build.patch
%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRequires:  java-rpmbuild >= 0:1.5, ant

%if %{gcj_support}
BuildRequires:       java-gcj-compat-devel
%endif

%description 
This package provides standardized, efficient versions of utility classes
commonly encountered in concurrent Java programming. This code consists of
implementations of ideas that have been around for ages, and is merely intended
to save you the trouble of coding them. Discussions of the rationale and
applications of several of these classes can be found in the second edition of
Concurrent Programming in Java.


%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -c -q
mkdir -p src/EDU/oswego/cs/dl/util
mv concurrent src/EDU/oswego/cs/dl/util
# Build with debug on
pushd src/EDU/oswego/cs/dl/util/concurrent
%patch0
popd

%build
pushd src/EDU/oswego/cs/dl/util/concurrent
%{ant} \
	-Dversion=%{version} \
	-Dj2se.apiurl=%{_javadocdir}/java \
	dist javadoc
popd

%install
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 src/EDU/oswego/cs/dl/util/concurrent/lib/%{name}.jar \
	%{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr src/EDU/oswego/cs/dl/util/concurrent/docs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%{_javadir}/*.jar
%doc src/EDU/oswego/cs/dl/util/concurrent/intro.html

%if %{gcj_support}
%{_libdir}/gcj/%{name}/concurrent-1.3.4.jar.*
%endif

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

