%{?_javapackages_macros:%_javapackages_macros}
# Copyright (c) 2000-2007, JPackage Project
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

Name:           concurrent
Version:        1.3.4
Release:        19.1
Epoch:          0
Summary:        Utility classes for concurrent Java programming
License:        Public Domain
Source0:        http://gee.cs.oswego.edu/dl/classes/EDU/oswego/cs/dl/current/concurrent.tar.gz
# Source1 not used, kept for reference
Source1:        %{name}-%{version}.build.xml
Source2:        %{name}-%{version}.pom
Patch0:         concurrent-build.patch
Patch1:         JDK-8-support.patch
URL:            http://gee.cs.oswego.edu/dl/classes/EDU/oswego/cs/dl/util/concurrent/intro.html
Group:          Development/Java

BuildArch:      noarch

BuildRequires:  jpackage-utils
BuildRequires:  ant
BuildRequires:  javapackages-local

Requires:       jpackage-utils

%description 
This package provides standardized, efficient versions of utility classes
commonly encountered in concurrent Java programming. This code consists of
implementations of ideas that have been around for ages, and is merely intended
to save you the trouble of coding them.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -c -q
mkdir -p src/EDU/oswego/cs/dl/util
mv concurrent src/EDU/oswego/cs/dl/util
# Build with debug on
pushd src/EDU/oswego/cs/dl/util/concurrent
%patch0
%patch1 -p1
popd
sed -i -e 's/..\/sun-u.c.license.pdf/http:\/\/gee.cs.oswego.edu\/dl\/classes\/EDU\/oswego\/cs\/dl\/util\/sun-u.c.license.pdf/' src/EDU/oswego/cs/dl/util/concurrent/intro.html

%build
pushd src/EDU/oswego/cs/dl/util/concurrent

ant \
  -Dversion=%{version} \
  -Dj2se.apiurl=%{_javadocdir}/java \
  dist javadoc

popd

%install
# JAR
%mvn_artifact %{SOURCE2} src/EDU/oswego/cs/dl/util/concurrent/lib/concurrent.jar

# JAVADOCS
%mvn_install -J src/EDU/oswego/cs/dl/util/concurrent/docs/

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc src/EDU/oswego/cs/dl/util/concurrent/intro.html

%files javadoc -f .mfiles-javadoc

%changelog
* Tue Jun 24 2014 Marek Goldmann <mgoldman@redhat.com> - 0:1.3.4-19
- Switch to javapackages-local

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 Marek Goldmann <mgoldman@redhat.com> - 0:1.3.4-14
- Added depmaps
- Removed gcj support

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.3.4-9
- drop repotag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.3.4-8jpp.1
- Autorebuild for GCC 4.3

* Thu Jan 10 2008 Permaine Cheung <pcheung at redhat.com> - 0:1.3.4-7jpp.1
- Merge with upstream version

* Fri Mar 16 2007 Permaine Cheung <pcheung at redhat.com> - 0:1.3.4-5jpp.1
- Merge with upstream version, update with the correct src tar ball

* Thu Aug 03 2006 Matt Wringe <mwringe at redhat.com> - 0:1.3.4-4jpp.1
- Merge with upstream version:
 - Add missing requires for javadoc task
 - Add missing postun for javadoc task

* Sun Jul 23 2006 Matt Wringe <mwringe at redhat.com> - 0:1.3.4-3jpp-5fc
- Rebuilt

* Sun Jul 23 2006 Matt Wringe <mwringe at redhat.com> - 0:1.3.4-3jpp_4fc
- Rebuilt

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.3.4-3jpp_3fc
- Rebuilt

* Thu Jul 20 2006 Matt Wringe <mwringe at redhat.com> - 0:1.3.4-3jpp_2fc
- Removed vendor and distribution tags

* Thu Jul 20 2006 Matt Wringe <mwringe at redhat.com> - 0:1.3.4-3jpp_1fc
- Merge with upstream version

* Thu Jul 20 2006 Matt Wringe <mwringe at redhat.com> - 0:1.3.4-3jpp
- Added conditional native compiling

* Thu Apr 27 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.3.4-2jpp
- First JPP 1.7 build

* Thu Dec 23 2004 Sebastiano Vigna <vigna@acm.org> 0:1.3.4-1jpp
- New release.

* Fri Aug 20 2004 Ralph Apel <r.apel at r-apel.de> 0:1.3.2-3jpp
- Build with ant-1.6.2

* Wed Nov 19 2003 Sebastiano Vigna <vigna@acm.org> 0:1.3.2-2jpp
- Package name restored to EDU.

* Wed Nov 19 2003 Sebastiano Vigna <vigna@acm.org> 0:1.3.2-1jpp
- First JPackage version

