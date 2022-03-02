%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^osgi\\($

Name:           xmvn
Version:        3.0.0
Release:        24
Summary:        Local Extensions for Apache Maven
License:        ASL 2.0
URL:            https://fedora-java.github.io/xmvn/
Source0:        https://github.com/fedora-java/xmvn/releases/download/%{version}/xmvn-%{version}.tar.xz
BuildArch:      noarch

Patch0000:      0001-Fix-installer-plugin-loading.patch
Patch0001:      0001-Port-to-Gradle-4.2.patch
Patch0002:      0001-Port-to-Gradle-4.3.1.patch
Patch0003:      0001-Support-setting-Xdoclint-none-in-m-javadoc-p-3.0.0.patch
Patch0004:      0001-Fix-configuration-of-aliased-plugins.patch
Patch0005:      0001-Don-t-use-JAXB-for-converting-bytes-to-hex-string.patch
Patch0006:      0001-Use-apache-commons-compress-for-manifest-injection-a.patch
Patch0007:      0001-Port-to-Gradle-4.4.1.patch

BuildRequires:  maven >= 3.5.0 maven-local apache-commons-compress beust-jcommander cglib
BuildRequires:  maven-dependency-plugin maven-plugin-build-helper maven-assembly-plugin
BuildRequires:  maven-install-plugin maven-plugin-plugin objectweb-asm modello xmlunit apache-ivy
BuildRequires:  junit easymock maven-invoker plexus-containers-container-default gradle >= 4.3.1
BuildRequires:  plexus-containers-component-annotations plexus-containers-component-metadata

Requires:       xmvn-minimal = %{version}-%{release} maven >= 3.4.0

%description
XMvn is a set of free software components that are useful in packaging Java software
whose build is managed by Apache Maven. It maintains a system-wide repository of artifacts.

%package        minimal
Summary:        A simplified version of xmvn
Requires:       maven-lib >= 3.4.0 xmvn-connector-aether = %{version}-%{release}
Requires:       xmvn-api = %{version}-%{release} xmvn-core = %{version}-%{release}
Requires:       apache-commons-cli apache-commons-lang3 atinject google-guice guava20
Requires:       maven-lib maven-resolver-api maven-resolver-impl maven-resolver-spi
Requires:       maven-resolver-util maven-wagon-provider-api plexus-cipher plexus-classworlds
Requires:       plexus-containers-component-annotations plexus-interpolation plexus-sec-dispatcher
Requires:       plexus-utils sisu-inject sisu-plexus slf4j

%description    minimal
This package provides minimal version of XMvn, but can't use remote repositories.

%package        parent-pom
Summary:        Provides XMvn Parent POM

%description    parent-pom
XMvn Parent is project model from which all other XMvn modules are inheriting.
It defines settings common to all XMvn modules.

%package        api
Summary:        Provides XMvn API
Obsoletes:      xmvn-launcher < 3.0.0

%description    api
This module contains public interface for functionality implemented by XMvn Core.

%package        core
Summary:        Provides XMvn Core

%description    core
XMvn Core module implements the essential functionality of XMvn such as resolution
of artifacts from system repository. XMvn core is needed by all other modules.

%package        connector-aether
Summary:        Provides XMvn Connector for Maven Resolver

%description    connector-aether
XMvn Connector for Eclipse Aether provides integration of Eclipse
Aether with XMvn. It provides an adapter which allows XMvn resolver
to be used as Aether workspace reader.

%package        connector-gradle
Summary:        Provides XMvn Connector for Gradle

%description    connector-gradle
XMvn Connector for Gradle provides integration of Gradle with XMvn.It
provides an adapter which allows XMvn resolver to be used as Gradle resolver.

%package        connector-ivy
Summary:        Provides XMvn Connector for Apache Ivy

%description    connector-ivy
XMvn Connector for Apache Ivy provides integration of Apache Ivy
with XMvn. It provides an adapter which allows XMvn resolver to
be used as Ivy resolver.

%package        mojo
Summary:        Provides XMvn MOJO

%description    mojo
XMvn MOJO is a Maven plugin, which consists of several MOJOs. Some goals
of these MOJOs are intended to be attached to default Maven lifecycle
when building packages, others can be calleddirectly from Maven command line.

%package        tools-pom
Summary:        Provides XMvn Tools POM

%description    tools-pom
XMvn Tools is parent POM for all XMvn tools. It holds configuration
common to all XMvn tools.

%package        resolve
Summary:        Provides XMvn Resolver
Requires:       javapackages-tools

%description    resolve
XMvn Resolver is a commald-line tool resolve Maven artifacts from system repositories.

%package        bisect
Summary:        Provides XMvn Bisect
Requires:       javapackages-tools

%description    bisect
This is a debugging tool that can diagnose build failures.

%package        subst
Summary:        Provides XMvn Subst
Requires:       javapackages-tools

%description    subst
This is a tool can substitute Maven artifact files with symbolic
links to corresponding files in artifact repository.

%package        install
Summary:        Provides XMvn Install
Requires:       apache-commons-compress
Requires:       javapackages-tools

%description    install
This is a command-line interface to XMvn installer.The installer reads
reactor metadata and performs artifact installation according to specified configuration.

%package        help
Summary:        Provides API documentation for xmvn
Requires:       xmvn = %{version}-%{release}
Provides:       xmvn-javadoc = %{version}-%{release}
Obsoletes:      xmvn-javadoc < %{version}-%{release}

%description    help
This package provides API documentation for xmvn

%prep
%autosetup -n xmvn-%{version} -p1

%pom_remove_plugin -r :maven-site-plugin
%mvn_package ":xmvn{,-it}" __noinstall
%pom_remove_plugin -r :apache-rat-plugin
%pom_remove_plugin -r :maven-checkstyle-plugin
%pom_remove_plugin -r :jacoco-maven-plugin
%pom_remove_plugin :jacoco-maven-plugin xmvn-it
%pom_xpath_remove "pom:executions/pom:execution[pom:id[text()='maven-binaries']]"
%pom_remove_plugin :maven-jar-plugin xmvn-tools
maven_home=$(realpath $(dirname $(realpath $(which mvn)))/..)
mver=$(sed -n '/<mavenVersion>/{s/.*>\(.*\)<.*/\1/;p}' \
           xmvn-parent/pom.xml)
install -d target/dependency/
cp -aL ${maven_home} target/dependency/apache-maven-$mver

sed -i 's/CONFIG\/2.0.0/METADATA\/3.0.0/g' xmvn-tools/xmvn-install/src/test/resources/test-pkg.xml
sed -i 's/CONFIG\/2.0.0/METADATA\/3.0.0/g' xmvn-tools/xmvn-install/src/test/resources/test-pkg-resolved.xml
sed -i 's/CONFIG\/2.0.0/METADATA\/3.0.0/g' xmvn-tools/xmvn-install/src/test/resources/test-pkg-main.xml
sed -i 's/CONFIG\/2.0.0/METADATA\/3.0.0/g' xmvn-tools/xmvn-install/src/test/resources/test-pkg-sub.xml

%build
%mvn_build -s -j

tar --delay-directory-restore -xvf target/*tar.bz2
chmod -R +rwX xmvn-%{version}*
rm -f xmvn-%{version}*/{AUTHORS-XMVN,README-XMVN.md,LICENSE,NOTICE,NOTICE-XMVN}
rm -Rf xmvn-%{version}*/lib/{installer,resolver,subst,bisect}/
rm -f xmvn-%{version}*/bin/*

%install
%mvn_install

maven_home=$(realpath $(dirname $(realpath $(which mvn)))/..)
install -d -m 755 %{buildroot}%{_datadir}/xmvn
cp -r xmvn-%{version}*/* %{buildroot}%{_datadir}/xmvn/

echo "#!/bin/sh -e
export _FEDORA_MAVEN_HOME=\"%{_datadir}/xmvn\"
exec ${maven_home}/bin/mvn \"\${@}\""> %{buildroot}%{_datadir}/xmvn/bin/mvn
echo "#!/bin/sh -e
export _FEDORA_MAVEN_HOME=\"%{_datadir}/xmvn\"
exec ${maven_home}/bin/mvnDebug \"\${@}\""> %{buildroot}%{_datadir}/xmvn/bin/mvnDebug

chmod 755 %{buildroot}%{_datadir}/xmvn/bin/mvn
chmod 755 %{buildroot}%{_datadir}/xmvn/bin/mvnDebug

%jpackage_script org.fedoraproject.xmvn.tools.bisect.BisectCli "" "-Dxmvn.home=%{_datadir}/xmvn" xmvn/xmvn-bisect:beust-jcommander:maven-invoker:plexus/utils xmvn-bisect
%jpackage_script org.fedoraproject.xmvn.tools.install.cli.InstallerCli "" "" xmvn/xmvn-install:xmvn/xmvn-api:xmvn/xmvn-core:beust-jcommander:slf4j/api:slf4j/simple:objectweb-asm/asm:commons-compress xmvn-install
%jpackage_script org.fedoraproject.xmvn.tools.resolve.ResolverCli "" "" xmvn/xmvn-resolve:xmvn/xmvn-api:xmvn/xmvn-core:beust-jcommander xmvn-resolve
%jpackage_script org.fedoraproject.xmvn.tools.subst.SubstCli "" "" xmvn/xmvn-subst:xmvn/xmvn-api:xmvn/xmvn-core:beust-jcommander xmvn-subst

cp -r ${maven_home}/lib/* %{buildroot}%{_datadir}/xmvn/lib/
xmvn-subst -s -R %{buildroot} %{buildroot}%{_datadir}/xmvn/
ln -s %{_datadir}/xmvn/bin/mvn %{buildroot}%{_bindir}/xmvn
ln -s xmvn %{buildroot}%{_bindir}/mvn-local
install -d -m 755 %{buildroot}%{_datadir}/xmvn/conf/
cp -P ${maven_home}/conf/settings.xml %{buildroot}%{_datadir}/xmvn/conf/
cp -P ${maven_home}/bin/m2.conf %{buildroot}%{_datadir}/xmvn/bin/

%files
%{_bindir}/mvn-local

%files minimal
%{_bindir}/xmvn
%dir %{_datadir}/xmvn
%dir %{_datadir}/xmvn/bin
%dir %{_datadir}/xmvn/lib
%{_datadir}/xmvn/lib/*.jar
%{_datadir}/xmvn/lib/ext
%{_datadir}/xmvn/lib/jansi-native
%{_datadir}/xmvn/bin/m2.conf
%{_datadir}/xmvn/bin/mvn
%{_datadir}/xmvn/bin/mvnDebug
%{_datadir}/xmvn/boot
%{_datadir}/xmvn/conf

%files parent-pom -f .mfiles-xmvn-parent
%doc LICENSE NOTICE

%files core -f .mfiles-xmvn-core

%files api -f .mfiles-xmvn-api
%doc AUTHORS README.md LICENSE NOTICE

%files connector-aether -f .mfiles-xmvn-connector-aether

%files connector-gradle -f .mfiles-xmvn-connector-gradle

%files connector-ivy -f .mfiles-xmvn-connector-ivy

%files mojo -f .mfiles-xmvn-mojo

%files tools-pom -f .mfiles-xmvn-tools

%files resolve -f .mfiles-xmvn-resolve
%{_bindir}/%{name}-resolve

%files bisect -f .mfiles-xmvn-bisect
%{_bindir}/%{name}-bisect

%files subst -f .mfiles-xmvn-subst
%{_bindir}/%{name}-subst

%files install -f .mfiles-xmvn-install
%{_bindir}/%{name}-install

%files help
%doc NOTICE

%changelog
* Mon Feb 28 2022 Ge Wang <wangge20@huawei.com> 3.0.0-24
- Modify tests file due to maven upgrade to version 3.6.3

* Mon Sep 14 2020 maminjie <maminjie1@huawei.com> 3.0.0-23
- Port to Gradle 4.4.1

* Fri Nov 22 2019 sunguoshuai <sunguoshuai@huawei.com> - 3.0.0-22
- Package init.
