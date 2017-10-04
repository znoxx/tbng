PANDOC=pandoc
TOCDEPTH=4
TEMPLATE=html5template
PANDOC_OPTIONS=-s --toc --toc-depth=$(TOCDEPTH) --template=$(TEMPLATE)

all: 00_RU 00_EN 01_RU 01_EN
.PHONY: all

00_RU : 
	$(PANDOC) $(PANDOC_OPTIONS) 00-tbng_overview_RU.md 00_RU_metadata.yaml  -o 00-tbng_overview_RU.html 

00_EN: 
	$(PANDOC) $(PANDOC_OPTIONS) 00-tbng_overview_EN.md 00_EN_metadata.yaml  -o 00-tbng_overview_EN.html 

01_RU : 
	$(PANDOC) $(PANDOC_OPTIONS) 01-tbng-install_and_setup_RU.md 01_RU_metadata.yaml  -o 01-tbng-install_and_setup_RU.html 

01_EN: 
	$(PANDOC) $(PANDOC_OPTIONS) 01-tbng-install_and_setup_EN.md 01_EN_metadata.yaml  -o 01-tbng-install_and_setup_EN.html 


clean:
	rm -f 00-tbng_overview_RU.html
	rm -f 00-tbng_overview_EN.html
	rm -f 01-tbng-install_and_setup_RU.html
	rm -f 01-tbng-install_and_setup_EN.html
