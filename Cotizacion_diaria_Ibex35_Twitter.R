#Autor : Tomás Castaño
#Descripción: Este Script scrapea la pagia de Yahoo finanzas del Ibex35, crea dos textos con las empresas con mas beneficios y perdidas y
# crea una gráfica de barras con los resultados
#
#

library(BatchGetSymbols)
library(prophet)
require(rvest)
require(magrittr)
library(quantmod)
library(twitteR)
library(rtweet)
library(lubridate)
#Conexion a twitter
############################################################################################################################################################
setup_twitter_oauth(consumer_key = "xxxxxxxxxxxxxxx",
                    access_token = "xxxxxxxxxxxxxxxx",
                    consumer_secret = "xxxxxxxxxxxxx",
                    access_secret = "xxxxxxxxxxxxxxxxxx")


#Recojemos los simbolos de Ibex 35
############################################################################################################################################################

url <- "https://es.finance.yahoo.com/quote/%5EIBEX/components?p=%5EIBEX"
# we save in the variable url the website url.
pagina <- read_html(url, as.data.frame=T, stringsAsFactors = TRUE)
#We crequire(magrittr)
#reate a function with read_html to read the web page.
pagina %>%  
  html_nodes("table") %>% 
  #Here, we indicate that this is the table we want to extract.
  .[[1]] %>% 
  #Here we put of which table of the HTML is about, in our example it is the third table of the web.
  html_table(fill=T) -> x
#We save it in a CSV.
#View(x)
#Look at the table if is correct.
#write.csv(x, "mis_datos_wikipedia.csv")

first.date <- Sys.Date()
last.date <- Sys.Date()
colnames(x)[1] <- "Symbol"

TotalResult <-data.frame()

for (i in 1:nrow(x)) {
  url <- paste0("https://es.finance.yahoo.com/quote/",x$Symbol[i],"/history?p=",x$Symbol[i])
  pagina <- read_html(url, as.data.frame=T, stringsAsFactors = TRUE)
  pagina %>%  
    html_nodes("table") %>% 
    #Here, we indicate that this is the table we want to extract.
    .[[1]] %>% 
    #Here we put of which table of the HTML is about, in our example it is the third table of the web.
    html_table(fill=T) -> result
  result <- data.frame(result)
  colnames(result)<- c("ref.date","price.open","price.high","price.low","price.close","price.adjusted","volume")
  #result$ref.date <- rownames(result)
  result$tickers <- x$Symbol[i]
  result$Company.name <- x$`Nombre de la empresa`[i]
  rownames(result) <- NULL
  TotalResult <- rbind(TotalResult, result)
}
TotalResult$ref.date <- gsub(" ene. ","-01-",TotalResult$ref.date)
TotalResult$ref.date <- gsub(" feb. ","-02-",TotalResult$ref.date)
TotalResult$ref.date <- gsub(" mar. ","-03-",TotalResult$ref.date)
TotalResult$ref.date <- gsub(" abr. ","-04-",TotalResult$ref.date)
TotalResult$ref.date <- gsub(" may. ","-05-",TotalResult$ref.date)
TotalResult$ref.date <- gsub(" jun. ","-06-",TotalResult$ref.date)
TotalResult$ref.date <- gsub(" jul. ","-07-",TotalResult$ref.date)
TotalResult$ref.date <- gsub(" ago. ","-08-",TotalResult$ref.date)
TotalResult$ref.date <- gsub(" sep. ","-09-",TotalResult$ref.date)
TotalResult$ref.date <- gsub(" oct. ","-10-",TotalResult$ref.date)
TotalResult$ref.date <- gsub(" nov. ","-11-",TotalResult$ref.date)
TotalResult$ref.date <- gsub(" dic. ","-12-",TotalResult$ref.date)
#TotalResult$ref.date <- as.Date(TotalResult$ref.date)
TotalResult$ref.date <- parse_date_time(TotalResult$ref.date, orders = "dmy")

TotalResult$price.open <- gsub(",",".",TotalResult$price.open)
TotalResult$price.high <- gsub(",",".",TotalResult$price.high)
TotalResult$price.low <- gsub(",",".",TotalResult$price.low)
TotalResult$price.close <- gsub(",",".",TotalResult$price.close)
TotalResult$price.adjusted <- gsub(",",".",TotalResult$price.adjusted)
TotalResult$volume <- gsub(",",".",TotalResult$volume)

TotalResult$price.open <- as.numeric(TotalResult$price.open)
class(TotalResult$price.open)
TotalResult$price.high <- as.numeric(TotalResult$price.high)
TotalResult$price.low <- as.numeric(TotalResult$price.low)
TotalResult$price.close <- as.numeric(TotalResult$price.close)
TotalResult$price.adjusted <- as.numeric(TotalResult$price.adjusted)
TotalResult$volume <- as.numeric(TotalResult$volume)
TotalResult$DayOfWeek <- weekdays(as.Date(TotalResult$ref.date))
TotalResult <- TotalResult[order(TotalResult$diff.percent, decreasing = TRUE),]

TotalResult$DayOfWeek <- gsub("Monday","Lunes",TotalResult$DayOfWeek)
TotalResult$DayOfWeek <- gsub("Tuesday","Martes",TotalResult$DayOfWeek)
TotalResult$DayOfWeek <- gsub("Wednesday","Miércoles",TotalResult$DayOfWeek)
TotalResult$DayOfWeek <- gsub("Thursday","Jueves",TotalResult$DayOfWeek)
TotalResult$DayOfWeek <- gsub("Friday","Viernes",TotalResult$DayOfWeek)
TotalResult$DayOfWeek <- gsub("Saturday","Sabado",TotalResult$DayOfWeek)
TotalResult$DayOfWeek <- gsub("Sunday","Domingo",TotalResult$DayOfWeek)

TotalResult$Company.name <- gsub(", S.A","",TotalResult$Company.name)


#Creamos el data set del día

TotalResultDaily <- subset(TotalResult, TotalResult$ref.date == last.date)
TotalResultDaily$dif <- round(TotalResultDaily$price.close - TotalResultDaily$price.open, 2)

TotalResultDaily$diff.percent <- round((((TotalResultDaily$price.close / TotalResultDaily$price.open)-1)*100),2)
TotalResultDaily <- TotalResultDaily[order(TotalResultDaily$diff.percent, decreasing = TRUE),]
#TotalResultDaily$diff.percent <- paste0(TotalResultDaily$diff.percent,"%")



DayOfWeek <- TotalResultDaily$DayOfWeek[1]
#Ordenamos 
#CINCO MEJORES/PEORES RESULTADOS DE HOY

BetterCotization <- head(TotalResultDaily, 5)
#TextoBetterCotization <- paste0("Resumen de la jornada del Ibex35 hoy ",DayOfWeek, ",día negro para la Bolsa Españolalas empresas que más han aumentado su cotización son: ",
                                
#Creamos el Texto
TextoBetterCotization <- HTML(paste0("Resumen de la jornada del Ibex35 hoy ",DayOfWeek, ", las 5 empresas que más han aumentado su valor son: ","\n",
                                BetterCotization$Company.name[1], " un ", BetterCotization$diff.percent[1],"%",", ","\n",
                                BetterCotization$Company.name[2], " un ", BetterCotization$diff.percent[2],"%",", ","\n",
                                BetterCotization$Company.name[3], " un ", BetterCotization$diff.percent[3],"%",", ","\n",
                                BetterCotization$Company.name[4], " un ", BetterCotization$diff.percent[4],"%"," y ","\n",
                                BetterCotization$Company.name[5], " un ", BetterCotization$diff.percent[5],"%"," #Ibex35"
)
)
nchar(TextoBetterCotization)
rtweet::post_tweet(TextoBetterCotization)

post_message(TextoBetterCotization, "@AIConsulting2", media = NULL, token = NULL)


WorstCotization <- tail(TotalResultDaily, 5)
#WorstCotization <- WorstCotization[order(WorstCotization$diff.percent, decreasing = FALSE),]

#Creamos el Texto
TextoWorstCotization <- HTML(paste0("Resumen de la jornada del Ibex35 hoy ",DayOfWeek, ",las 5 empresas que más valor han perdido son: ","\n",
                               WorstCotization$Company.name[1], " : ", WorstCotization$diff.percent[1],"%",", ","\n",
                               WorstCotization$Company.name[2], " : ", WorstCotization$diff.percent[2],"%",", ","\n",
                               WorstCotization$Company.name[3], " : ", WorstCotization$diff.percent[3],"%",", ","\n",
                               WorstCotization$Company.name[4], " : ", WorstCotization$diff.percent[4],"%"," y ","\n",
                               WorstCotization$Company.name[5], " : ", WorstCotization$diff.percent[5],"%"," #Ibex35"
)
)
nchar(TextoWorstCotization)
rtweet::post_tweet(TextoWorstCotization)


#Visualización de datos
library(ggplot2)
# Diverging Barcharts
TotalResultDaily$diff_type <- ifelse(TotalResultDaily$diff.percent < 0, "below", "above")  # above / below avg flag
TotalResultDaily$Company.name <- factor(TotalResultDaily$Company.name, levels = TotalResultDaily$Company.name)  # convert to factor to retain sorted order in plot.
#Renombramos las columans para su visualización
colnames(TotalResultDaily)[9] <- "Compañía"
colnames(TotalResultDaily)[12] <- "Variación Porcentual"
Imagen1 <- ggplot(TotalResultDaily, aes(x=Compañía, y=`Variación Porcentual`, label=`Variación Porcentual`)) + 
                  geom_bar(stat='identity', aes(fill=diff_type), width=.5)  +
                  scale_fill_manual(name="Variación", 
                    labels = c("Incremento de valor", "Disminución del valor"), 
                    values = c("above"="#00ba38", "below"="#f8766d")) + 
                  labs(subtitle=last.date, 
                  title= "Porcentaje de variación del valor de las acciones") + 
                  coord_flip()

Imagen1
filename <-paste0("Ibex35-barh-Variacion-",last.date,".png")
path ="~/Proyectos/Twitter/Finance_Tweets/Graficas"
ggsave(filename, path = path)

pathsend ="~/Proyectos/Twitter/Finance_Tweets/Graficas/"

post_tweet(status = paste0("Evolución del precio de cotización del Ibex35 del ",last.date," #Ibex35"),
          media = paste0(pathsend,filename),)
