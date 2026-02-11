1. Add this to the end of /usr/share/X11/xkb/symbols/us
```

partial alphanumeric_keys
xkb_symbols "brando" {
    include "us(basic)"
    name[Group1]= "Brando";

    // Your custom mappings
    key <AD03>  {[       f,      F              ]};
    key <AD04>  {[       p,      P              ]};
    key <AD05>  {[       g,      G              ]};
    key <AD06>  {[       j,      J              ]};
    key <AD07>  {[       l,      L              ]};
    key <AD08>  {[       u,      U              ]};
    key <AD09>  {[       y,      Y              ]};
    key <AD10>  {[       semicolon,      colon          ]};
    
    key <AC04>  {[       t,      T              ]};
    key <AC05>  {[       r,      R              ]};
    key <AC06>  {[       h,      H              ]};
    key <AC07>  {[       n,      N              ]};
    key <AC08>  {[       e,      E              ]};
    key <AC09>  {[       i,      I              ]};
    key <AC10>  {[       o,      O              ]};
    
    key <AB05>  {[       b,      B              ]};
    key <AB06>  {[       k,      K              ]};
    key <AB07>  {[       m,      M              ]};
};
```

2. Register it in the layout list by
```bash
sudo vim /usr/share/X11/xkb/rules/evdev.xml 
#or
code /usr/share/X11/xkb/rules/evdev.xml
```

add this:
```xml
  <variant>
    <configItem>
      <name>brando</name>
      <description>Brando</description>
    </configItem>
  </variant>
```
in this spot:
```xml
<layout>
  <configItem>
    <name>us</name>
    <!-- Keyboard indicator for English layouts -->
    <shortDescription>en</shortDescription>
    <description>English (US)</description>
    <countryList>
      <iso3166Id>US</iso3166Id>
    </countryList>
    <languageList>
      <iso639Id>eng</iso639Id>
    </languageList>
  </configItem>
  <variantList>

    <!--  -->
    <!-- HERE -->
    <!--  -->

    <variant>
      <configItem>
        <name>euro</name>
        <description>English (US, euro on 5)</description>
      </configItem>
    </variant>

    ....
```

3. clear the cache
```bash
sudo rm -rf /var/lib/xkb/*
```

4. restart your system and then look for your layout in the keyboard settings



