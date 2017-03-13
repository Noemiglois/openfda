#BIBLIOTECA
#https://github.com/acs/python-red/blob/master/webserver/server.py
import http.client
import http.server
import json

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    OPENFDA_API_URL='api.fda.gov'
    OPENFDA_API_EVENT="/drug/event.json"
    def get_events(self):
        conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)  #conexion
        conn.request('GET', self.OPENFDA_API_EVENT+'?limit=10') #GET hace un peticion y la respuesta se almacena en la biblioteca
        r1= conn.getresponse()  #recupera la respuesta y la almacena en una variable
        #print(r1.status, r1.reason)
        data1=r1.read()
        data1=data1.decode('utf8') #me lo decodificas a un string con formato utf8 (c es el 99, a es el 45...y se transforman en 0s y 1s)
        events=json.loads(data1) #de string a diccionario
        return events

    def get_events_search(self):
        print('get_events_search')
        conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)  #conexion
        conn.request("GET", self.OPENFDA_API_EVENT+ "?limit=10&search=patient.drug.medicinalproduct:LYRICA") #GET hace un peticion y la respuesta se almacena en la biblioteca
        r1= conn.getresponse()  #recupera la respuesta y la almacena en una variable
        data1=r1.read()
        data1=data1.decode('utf8') #me lo decodificas a un string con formato utf8 (c es el 99, a es el 45...y se transforman en 0s y 1s)
        events=json.loads(data1) #de string a diccionario
        return events

    def get_main_page(self):
        html= """
        <html>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1>OpenFDA Client</h1>
                <form method="get" action="receive">
                    <input type="submit" value="Enviar a OpenFDA">
                    </input>
                </form>
                <form method= 'get' action='search'>
                    <input type='submit' value='Buscar'>
                    </input>
                </form>
            </body>
        </html>
        """
        return html

    def get_drugs_from_events(self, events):
        drugs=[]
        for event in events:
            drug=event['patient']['drug'][0]['medicinalproduct']
            drugs+=[drug]
        return drugs

    def get_drugs(self, drugs):
        html2='''
        <html>
            <head>
                <tittle>OpenFda Cool App</tittle>
            </head>
            <body>
                <ul type="square">
        '''
        for drug in drugs:
            html2+="<li>"+drug+"</li>\n"

        html2 += '''
                </ul>
            </body>
        </html>
        '''
        return html2

    def get_companies_name(self, companies):
        html3='''
        <html>
            <head>
                <tittle>OpenFda Cool App</tittle>
            </head>
            <body>
                <ul type="square">
        '''
        for company in companies:
            html3+="<li>"+company+"</li>\n"

        html3 += '''
                </ul>
            </body>
        </html>
        '''
        return html3


    def get_companies_from_events(self, events):
        companies=[]
        for event in events:
            companies+=[event['companynumb']]
        return companies

    def do_GET(self):
        main_page=False
        is_event=False
        is_search=False
        if self.path=='/':
            main_page= True
        elif self.path== '/receive?':
            is_event= True
        elif self.path=='/search?':
            print ('is_search=True')
            is_search= True
        self.send_response(200) #send response status code
        self.send_header('Content-type', 'text/html') #oye cliente, lo que te voy a enviar esta en formato html
        self.end_headers()
        html=self.get_main_page()

        if main_page:
            self.wfile.write(bytes(html,'utf8')) #ESTE ES EL COMANDO DE ENVIO
        elif is_event:
            events=self.get_events()
            events=events['results']
            drugs=self.get_drugs_from_events(events)
            html=self.get_drugs(drugs)
            self.wfile.write(bytes(html,'utf8')) #ESTE ES EL COMANDO DE ENVIO
        elif is_search:
            events=self.get_events_search()
            events=events['results']
            companies=self.get_companies_from_events(events)
            html=self.get_companies_name(companies)
            self.wfile.write(bytes(html,'utf8')) #ESTE ES EL COMANDO DE ENVIO
        return
