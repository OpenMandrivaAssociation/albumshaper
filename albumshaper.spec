Name: albumshaper
Version: 2.1
Release: %mkrel 5
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
BuildRequires: ImageMagick

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


