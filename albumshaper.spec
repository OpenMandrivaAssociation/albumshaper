Name: albumshaper
Version: 2.1
Release: %mkrel 9
License: GPL
Url: http://albumshaper.sf.net
Group: Graphics
Source: http://prdownloads.sourceforge.net/albumshaper/%{name}_%{version}.tar.bz2
#gw disable upx, find-requires is broken
Patch: albumshaper-2.1-no-upx.patch
Patch1: albumshaper-2.1-gcc4.1.patch
Summary: Graphical application used to create, maintain, and share photo albums
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libxslt-devel doxygen
BuildRequires: qt3-devel
#upx
BuildRequires: imagemagick

%description
Album Shaper is a graphical application used to create, maintain, and
share photo albums using open formats like HTML, XSLT, and JPG.
Two-layer albums can be created in a drag-n-drop interface which
allows quick and easy arrangement and catagorization of photos. Batch
rotations make getting your photos ready a quick and easy task. You
can also crop, enhance, and manipulate your photos using a powerful
but intuitive editing interface. Photos, collections, and albums
themselves can be labeled as needed and modified at a later time by
saving and loading from a simple XML format. Albums are exported as
HTML which can then be posted directly on the web or viewed straight
from your hard drive. Album Shaper now supports themes which means you
can completely customize the look of the Albums you produce! Album
Shaper is designed to help you share your photos with your friends and
family as easily as possible, as well as update and maintain these
Albums in the most effecient and easy way possible.

%prep
%setup -q -n %{name}_%{version}_src
%patch -p1
%patch1 -p1
for file in AlbumShaper.pro AlbumShaper.xcode/project.pbxproj src/main.cpp
do
  sed -i -e 's|/local||g' $file
done
qmake

%build
%make
doxygen AlbumShaper.doc

%install
/bin/rm -rf %{buildroot}

# Install to rpm build location
%makeinstall INSTALL_ROOT=%{buildroot}
install -m 755 bin/AlbumShaper %buildroot%_bindir/AlbumShaper
find %buildroot -name .DS_Store -exec rm {} \;
find %buildroot%_datadir -type f -exec chmod 644 {} \;

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=AlbumShaper
Comment=Create photo albums
Exec=%{_bindir}/AlbumShaper
Icon=%name
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-Multimedia-Graphics;Photography;Graphics;Viewer;
EOF
mkdir -p %buildroot{%_liconsdir,%_miconsdir}
convert -scale 48 resources/icons/as64.png %buildroot%_liconsdir/%name.png
install -m 644 resources/icons/as32.png %buildroot%_iconsdir/%name.png
install -m 644 resources/icons/as16.png %buildroot%_miconsdir/%name.png

%clean
rm -rf $RPM_BUILD_ROOT/

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files
%defattr(-,root,root)
%doc docs/html docs/bugs.txt docs/copying.txt *.txt
%_bindir/*
%_datadir/%name
%_datadir/applications/mandriva*
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png




%changelog
* Tue Dec 06 2011 GÃ¶tz Waschk <waschk@mandriva.org> 2.1-9mdv2012.0
+ Revision: 738095
- yearly rebuild

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1-8mdv2011.0
+ Revision: 609963
- rebuild

* Thu Jan 14 2010 Funda Wang <fwang@mandriva.org> 2.1-7mdv2010.1
+ Revision: 491116
- rebuild for libjpeg v8

* Sun Aug 23 2009 Funda Wang <fwang@mandriva.org> 2.1-6mdv2010.0
+ Revision: 419743
- rebuild for libjpeg v7

* Thu Dec 11 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1-5mdv2010.0
+ Revision: 312987
- lowercase ImageMagick

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 2.1-5mdv2009.0
+ Revision: 218437
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Thierry Vignaud <tv@mandriva.org>
    - fix spacing at top of description
    - drop old menu

* Thu Dec 20 2007 Olivier Blin <blino@mandriva.org> 2.1-5mdv2008.1
+ Revision: 135819
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'


* Wed Jan 24 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.1-5mdv2007.0
+ Revision: 112779
- Import albumshaper

* Wed Jan 24 2007 Götz Waschk <waschk@mandriva.org> 2.1-5mdv2007.1
- unpack patches

* Fri Aug 25 2006 Götz Waschk <waschk@mandriva.org> 2.1-4mdv2007.0
- xdg menu

* Fri Aug 25 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.1-1mdv2007.0
- Rebuild

* Fri Jun 02 2006 Götz Waschk <waschk@mandriva.org> 2.1-3mdv2007.0
- patch1: fix build

* Thu Apr 13 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.1-2mdk
- Rebuild
- use mkrel

* Tue Apr 12 2005 Götz Waschk <waschk@linux-mandrake.com> 2.1-1mdk
- update the patch
- New release 2.1

* Wed Mar 16 2005 Götz Waschk <waschk@linux-mandrake.com> 2.0-1mdk
- initial package

