PANDOC=pandoc
TOCDEPTH=4
TEMPLATE=html5template
PANDOC_OPTIONS=-s --toc --toc-depth=$(TOCDEPTH) --template=$(TEMPLATE)

all: 00_RU 00_EN
.PHONY: all

00_RU : 
	$(PANDOC) $(PANDOC_OPTIONS) 00-tbng_overview_RU.md 00_RU_metadata.yaml  -o 00-tbng_overview_RU.html 

00_EN: 
	$(PANDOC) $(PANDOC_OPTIONS) 00-tbng_overview_EN.md 00_EN_metadata.yaml  -o 00-tbng_overview_EN.html 

clean:
	rm -f 00-tbng_overview_RU.html
	rm -f 00-tbng_overview_EN.html

