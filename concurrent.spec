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
Release:        %mkrel 7.0.9
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
rm -fr $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 src/EDU/oswego/cs/dl/util/concurrent/lib/%{name}.jar \
               $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr src/EDU/oswego/cs/dl/util/concurrent/docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

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


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.3.4-7.0.7mdv2011.0
+ Revision: 663397
- mass rebuild

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.3.4-7.0.6mdv2011.0
+ Revision: 603850
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.3.4-7.0.5mdv2010.1
+ Revision: 522403
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0:1.3.4-7.0.4mdv2010.0
+ Revision: 413267
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.3.4-7.0.3mdv2009.1
+ Revision: 350738
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:1.3.4-7.0.2mdv2009.0
+ Revision: 136335
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.3.4-7.0.2mdv2008.1
+ Revision: 120854
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sun Dec 09 2007 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.3.4-7.0.1mdv2008.1
+ Revision: 116771
- bump release
- use provided build.xml (sync with jpp)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.3.4-5.1.2mdv2008.0
+ Revision: 87296
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Wed Jul 04 2007 David Walluck <walluck@mandriva.org> 0:1.3.4-5.1.1mdv2008.0
+ Revision: 47910
- Import concurrent



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
