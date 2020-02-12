
library(ggplot2)
library(dplyr)
library(forcats)
library(stringr)
library(yaml)

data <- read.csv("data/intermediate/fixedScales.csv",stringsAsFactors = FALSE)
colors <- yaml.load_file("data/priocolors.yaml")

fixnames <- function(name){
   str_to_title(name) %>%
      str_replace_all("_"," ")
}
data$DEPTO <- fixnames(data$DEPTO)

print(max(data$P35conv+1,na.rm = T))

sumdata <- data %>%
   group_by(DEPTO) %>%
   summarize(sat = mean(P35conv + 1,na.rm = T))

overallmean <- mean(sumdata$sat,na.rm = T)

plt <- sumdata %>%
   ggplot(aes(x=fct_reorder(DEPTO,sat),y=sat,fill=DEPTO=="Arauca"))+
      geom_col() +
      coord_flip(ylim = c(1,4)) +
      geom_hline(yintercept=overallmean, alpha = 0.8, color = colors$darkblue) + 
      theme_classic() + 
      theme(text = element_text(size = 9), legend.position = "none",
         panel.grid.minor.x = element_line(color = colors$gray,size = 0.2),
         panel.grid.major.x = element_line(color = colors$gray)) +
      scale_fill_manual(values=c(colors$gray,colors$lightblue)) +
      scale_y_continuous(breaks = seq(1,4,1)) +
      labs(x = "Departamento", y= "Satisfacción")



ggsave("/tmp/plot.png",plt,height = 3.8, width = 6,device = "png")

