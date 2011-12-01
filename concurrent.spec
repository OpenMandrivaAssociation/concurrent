# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _with_gcj_support 1

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

Name:           concurrent
Version:        1.3.4
Release:        %mkrel 7.0.7
Epoch:          0
Summary:        Utility classes for concurrent Java programming
License:        Public Domain
Source0:        http://gee.cs.oswego.edu/dl/classes/EDU/oswego/cs/dl/current/concurrent.tar.gz
Source1:        %{name}-%{version}.build.xml
Patch0:         concurrent-build.patch
URL:            http://gee.cs.oswego.edu/dl/classes/EDU/oswego/cs/dl/util/concurrent/intro.html
Group:          Development/Java
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
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
rm -fr %{buildroot}
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

%clean
rm -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/*.jar
%doc src/EDU/oswego/cs/dl/util/concurrent/intro.html

%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/concurrent-1.3.4.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
