# Kamergotchi-Python
Dit script kan jouw Kamergotchi (in mijn geval Emile Roemer) automatiseren. Hierdoor is Emile Roemer altijd tevreden, heeft hij nooit honger, heeft hij genoeg aandacht en heeft hij een overvloed aan kennis.
Een ander bijkomend voordeel is dat jouw Kamergotchi in de ranglijsten komt te staan! Opvallend is dat het grote deel van de personen in de ranglijst Software Engineers zijn of een Software Development bedrijf representeren. Gek.

## Regels
Alhoewel het script tegen [de regels van kamergotchi](https://web.archive.org/web/20170221212443/http://www.kamergotchi.nl/faq/) is, heeft het een goede 2 dagen gewerkt voordat m'n account geblokkeerd werd.
Zodra je account geblokkeerd is krijg je een HTTP 403 met als melding _user is blocked_

## Gebruik
Via BurpSuite of [een Packet Capture app](https://play.google.com/store/apps/details?id=app.greyshirts.sslcapture) wil je de benodigde headers achterhalen. De app stuurt namelijk de device-id mee als een soort gebruikersnaam om jouw account te identificeren. Of het token nodig is weet ik niet.
Als je de app gebruikt kan je heel makkelijk je *device-id* en het *token* kopieren en plakken in het scriptje.
Daarna is het scriptje klaar voor gebruik en kan je deze runnen.

## Known Issues
In een enkel geval zal de server van kamergotchi een 502 Time-out returnen of een andere error. Het scriptje zal dan automatisch stoppen, maar voel je vrij om dit aan te passen zodat het scriptje zichzelf hervat!

## Resultaten
[Klik hier](https://web.archive.org/web/20170221211845/http://www.kamergotchi.nl/ranglijst/) voor de dag ranglijst.
[Klik hier](https://web.archive.org/web/20170221211828/http://www.kamergotchi.nl/totaal-ranglijst/) voor de totaal ranglijst
![totaal-ranglijst](http://i.imgur.com/OyyT76Ql.png) ![dag-ranglijst](http://i.imgur.com/x0odavPl.png)

## Werking van Kamergotchi
De kamergotchi app maakt, aan de achterkant, allemaal HTTPS requests naar een server. Hierdoor gebeurt alle logica op de server en is het niet mogelijk om lokaal de app te _hacken_ door bijvoorbeeld het memory aan te passen.
Wel kan je hierdoor heel makkelijk zelf de HTTPS requests uitvoeren, vanaf bijvoorbeeld een Python scriptje. Hieronder vind je alle HTTPS requests.
- POST /players/register & POST /game/start worden uitgevoerd bij het opstarten van het spel voor de eerste keer.
- POST /players/register-push wordt uitgevoerd bij het opstarten voor bijvoorbeeld de 2e keer. Waarschijnlijk is dit nodig voor het ontvangen van push berichten.
- GET /game wordt uitgevoerd om de huidige gamestatus te krijgen.
- POST /game/care is voor het geven van eten, aandacht en kennis.
- POST /game/claim is voor het claimen van de periodieke bonus.

### Aanmaken van een account
Request:
> POST /players/register HTTP/1.1  
> accept: application/json, text/plain, \*/\*  
> x-player-token: android:DEVICE-ID-HERE  
> Content-Type: application/json;charset=utf-8  
> Content-Length: 117  
> Host: api.kamergotchi.nl  
> Connection: Keep-Alive  
> Accept-Encoding: gzip  
> User-Agent: okhttp/3.4.1  
>   
> {"registration":{"nickname":"NAME","age":20,"gender":"male","supportCode":null,"token":"android:DEVICE-ID-HERE"}}  

Response:  
> HTTP/1.1 200 OK  
> Server: nginx/1.6.2  
> Date: Wed, 22 Feb 2017 09:40:03 GMT  
> Content-Type: application/json; charset=utf-8  
> Content-Length: 699  
> Connection: keep-alive  
> X-Powered-By: Express  
> Access-Control-Allow-Origin: *  
> Cache-Control: no-cache, private, no-store, must-revalidate, max-stale=0, post-check=0, pre-check=0  
> ETag: W/"2bb-agomljyMHwy+n7kTf4TQaw"  
>  
> {"player":{"currentGame":{"claimReset":null,"careLeft":10,"endDate":null,"startDate":null,"gotchi":{"partyText":"de PVV","party":"PVV","displayName":"Geert","name":"geert","public":true,"id":"\*\*\*\*\*\*\*\*\*"},"batchNumber":2,"player":"\*\*\*\*\*\*\*\*\*1","quotes":[],"dayScore":0,"score":0,"current":{"food":29,"attention":61,"knowledge":60},"device":null,"daysAlive":0,"health":50,"active":false,"ended":false,"started":false,"claimLimitSeconds":7200,"careLimitSeconds":420,"id":"\*\*\*\*\*\*\*\*\*"},"gender":"male","age":20,"blocked":false,"code":"\*\*\*\*","nickname":"NAME","token":"android:DEVICE-ID-HERE","endedGames":[],"device":null,"id":"\*\*\*\*\*\*\*\*\*"}}

### Spelinformatie krijgen
Request:
> GET /game HTTP/1.1  
> accept: application/json, text/plain, \*/\*  
> x-player-token: android:DEVICE-ID-HERE  
> Host: api.kamergotchi.nl  
> Connection: Keep-Alive  
> Accept-Encoding: gzip  
> User-Agent: okhttp/3.4.1  

Response:
> HTTP/1.1 200 OK  
> Server: nginx/1.6.2  
> Date: Wed, 22 Feb 2017 09:40:04 GMT  
> Content-Type: application/json; charset=utf-8  
> Content-Length: 507  
> Connection: keep-alive  
> X-Powered-By: Express  
> Access-Control-Allow-Origin: *  
> Cache-Control: no-cache, private, no-store, must-revalidate, max-stale=0, post-check=0, pre-check=0  
> ETag: W/"1fb-TEmjBqm62IeH6w+zcCQPpA"  
>   
> {"game":{"claimReset":null,"careLeft":10,"endDate":null,"startDate":null,"gotchi":{"partyText":"de PVV","party":"PVV","displayName":"Geert","name":"geert","public":true,"id":"\*\*\*\*\*\*\*\*\*"},"batchNumber":2,"player":"\*\*\*\*\*\*\*\*\*","quotes":[],"dayScore":0,"score":0,"current":{"food":29,"attention":61,"knowledge":60},"device":null,"daysAlive":0,"health":50,"active":false,"ended":false,"started":false,"claimLimitSeconds":7200,"careLimitSeconds":420,"id":"\*\*\*\*\*\*\*\*\*"}}  

### Eten, Aandacht of Kennis geven
Request:
> POST /game/care HTTP/1.1  
> accept: application/json, text/plain, \*/\*  
> x-player-token: android:DEVICE-ID-HERE  
> Content-Type: application/json;charset=utf-8  
> Content-Length: 19  
> Host: api.kamergotchi.nl  
> Connection: Keep-Alive  
> Accept-Encoding: gzip  
> User-Agent: okhttp/3.4.1  
>   
> {"bar":"attention"}  # Dit kan verandert worden door Food, Attention en Knowledge

Response:
> HTTP/1.1 200 OK  
> Server: nginx/1.6.2  
> Date: Wed, 22 Feb 2017 09:40:17 GMT  
> Content-Type: application/json; charset=utf-8  
> Content-Length: 728  
> Connection: keep-alive  
> X-Powered-By: Express  
> Access-Control-Allow-Origin: *  
> Cache-Control: no-cache, private, no-store, must-revalidate, max-stale=0, post-check=0, pre-check=0  
> ETag: W/"2d8-OXUJrICvP85LipgSut0WbQ"  
>   
> {"game":{"claimReset":"2017-02-22T11:40:15.530Z","careLeft":8,"endDate":null,"startDate":"2017-02-22T09:40:10.422Z","gotchi":{"partyText":"de PVV","party":"PVV","displayName":"Geert","name":"geert","public":true,"id":"\*\*\*\*\*\*\*\*\*"},"batchNumber":2,"player":"\*\*\*\*\*\*\*\*\*","careReset":"2017-02-22T09:47:16.898Z","quotes":[{"text":"Wauw!","sound":"thanksAttention","callout":"thanks","group":"attention","_id":"\*\*\*\*\*\*\*\*\*","replaces":["attention"]}],"dayScore":60,"score":60,"current":{"food":33,"attention":63,"knowledge":60},"device":null,"daysAlive":1,"health":52,"active":true,"ended":false,"started":true,"claimLimitSeconds":7200,"careLimitSeconds":420,"id":"\*\*\*\*\*\*\*\*\*"}}  

### Claimen van bonus
Request:
> POST /game/claim HTTP/1.1  
> accept: application/json, text/plain, \*/\*  
> x-player-token: android:DEVICE-ID-HERE  
> Content-Length: 0  
> Host: api.kamergotchi.nl  
> Connection: Keep-Alive  
> Accept-Encoding: gzip  
> User-Agent: okhttp/3.4.1  

Response:
> HTTP/1.1 200 OK  
> Server: nginx/1.6.2  
> Date: Wed, 22 Feb 2017 09:40:15 GMT  
> Content-Type: application/json; charset=utf-8  
> Content-Length: 669  
> Connection: keep-alive  
> X-Powered-By: Express  
> Access-Control-Allow-Origin: *  
> Cache-Control: no-cache, private, no-store, must-revalidate, max-stale=0, post-check=0, pre-check=0  
> ETag: W/"29d-i7z1aPi/PXiYmokP4j11Rg"  
>   
> {"game":{"claimReset":"2017-02-22T11:40:15.530Z","careLeft":10,"endDate":null,"startDate":"2017-02-22T09:40:10.422Z","gotchi":{"partyText":"de PVV","party":"PVV","displayName":"Geert","name":"geert","public":true,"id":"\*\*\*\*\*\*\*\*\*"},"batchNumber":2,"player":"\*\*\*\*\*\*\*\*\*","quotes":[{"text":"Ik heb honger","group":"food","sound":"weeh","callout":"need","_id":"\*\*\*\*\*\*\*\*\*","replaces":[]}],"dayScore":50,"score":50,"current":{"food":29,"attention":61,"knowledge":60},"device":null,"daysAlive":1,"health":50,"active":true,"ended":false,"started":true,"claimLimitSeconds":7200,"careLimitSeconds":420,"id":"\*\*\*\*\*\*\*\*\*"}}  

\- Robin
