import http.client
import http.server
import json

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    OPENFDA_API_URL='api.fda.gov'
    OPENFDA_API_EVENT="/drug/event.json"
    def get_events(self, limit):
        conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)  #conexion
        conn.request('GET', self.OPENFDA_API_EVENT+'?limit='+str(limit)) #GET hace un peticion y la respuesta se almacena en la biblioteca
        r1= conn.getresponse()  #recupera la respuesta y la almacena en una variable
        data1=r1.read()
        data1=data1.decode('utf8') #me lo decodificas a un string con formato utf8 (c es el 99, a es el 45...y se transforman en 0s y 1s)
        events=json.loads(data1) #de string a diccionario
        return events

    def get_events_search_drugs(self):
        conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)  #conexion
        drug=self.path.split('=')[1]
        conn.request("GET", self.OPENFDA_API_EVENT+ "?limit=10&search=patient.drug.medicinalproduct:" + drug) #GET hace un peticion y la respuesta se almacena en la biblioteca
        r1= conn.getresponse()  #recupera la respuesta y la almacena en una variable
        data1=r1.read()
        data1=data1.decode('utf8') #me lo decodificas a un string con formato utf8 (c es el 99, a es el 45...y se transforman en 0s y 1s)
        events=json.loads(data1) #de string a diccionario
        return events

    def get_events_search_companies(self):
        conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)  #conexion
        company=self.path.split('=')[1]
        conn.request("GET", self.OPENFDA_API_EVENT+ "?limit=10&search=companynumb:" + company) #GET hace un peticion y la respuesta se almacena en la biblioteca
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
            <body style="background:#23B57D">
            <span style="color:#FFBC03">

                <h1>OpenFDA Client</h1>

                <form method="get" action="listDrugs">
                    <input type="submit" value="Lista medicamentos">
                    </input>
                    <input type="text" name="Limit">
                    </input>
                </form>

                <form method="get" action="listCompanies">
                    <input type="submit" value="Lista de companias">
                    </input>
                    <input type="text" name="Limit">
                    </input>
                </form>

                <form method= "get" action="searchDrug">
                    <input type="text" name="drug">
                    </input>
                    <input type="submit" value="Buscar medicamentos">
                    </input>
                </form>

                <form method= 'get' action='searchCompany'>
                    <input type='text' name='company'>
                    </input>
                    <input type='submit' value='Buscar companias'>
                    </input>
                </form>

                <form method= 'get' action='listGender'>
                    <input type='text' name='Limit'>
                    </input>
                    <input type='submit' value='Generos'>
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

    def get_drugs(self, drugs): #LISTA DE MEDICAMENTOS
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

    def get_companies_name(self, companies):    #LISTA DE COMPAÑIAS
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

    def get_patientsex(self, events):
        patient_sex=[]
        for event in events:
            sex=event['patient']['patientsex']
            patient_sex+=[sex]

        return patient_sex

    def get_patientsex_html(self, patient_sex):    #LISTA DE SEXOS
        html4='''
        <html>
            <head>
                <tittle>OpenFda Cool App</tittle>
            </head>
            <body>
                <ul type="square">
        '''
        for sex in patient_sex:
            html4+="<li>"+sex+"</li>\n"

        html4 += '''
                </ul>
            </body>
        </html>
        '''
        return html4

    def get_companies_from_events(self, events):
        companies=[]
        for event in events:
            companies+=[event['companynumb']]
        return companies

    def do_GET(self):
        main_page=False
        is_event=False
        is_search1=False
        is_company=False
        is_search2= False
        patient_sex= False
        if self.path=='/':
            main_page= True
        elif 'listDrugs' in self.path:
            is_event= True
        elif 'searchDrug' in self.path:
            is_search1= True
        elif 'listCompanies' in self.path:
            is_company= True
        elif 'searchCompany' in self.path:
            is_search2= True
        elif 'listGender' in self.path:
            patient_sex=True

        self.send_response(200) #send response status code
        self.send_header('Content-type', 'text/html') #oye cliente, lo que te voy a enviar esta en formato html
        self.end_headers()
        html=self.get_main_page()

        if main_page:
            self.wfile.write(bytes(html,'utf8')) #ESTE ES EL COMANDO DE ENVIO
        elif is_event:
            limit= self.path.split('=')[1]
            if limit=='':
                limit=10
            events=self.get_events(str(limit))
            events=events['results']
            drugs=self.get_drugs_from_events(events)
            html=self.get_drugs(drugs)
            self.wfile.write(bytes(html,'utf8')) #ESTE ES EL COMANDO DE ENVIO
        elif is_search1:
            events=self.get_events_search_drugs()
            events=events['results']
            companies=self.get_companies_from_events(events)
            html=self.get_companies_name(companies)
            self.wfile.write(bytes(html,'utf8')) #ESTE ES EL COMANDO DE ENVIO
        elif is_company:
            limit= self.path.split('=')[1]
            if limit=='':
                limit=10
            events=self.get_events(str(limit))
            events=events['results']
            companies= self.get_companies_from_events(events)
            html=self.get_companies_name(companies)
            self.wfile.write(bytes(html,'utf8')) #ESTE ES EL COMANDO DE ENVIO
        elif is_search2:
            events=self.get_events_search_companies()
            events=events['results']
            drugs=self.get_drugs_from_events(events)
            html=self.get_drugs(drugs)
            self.wfile.write(bytes(html,'utf8')) #ESTE ES EL COMANDO DE ENVIO
        elif patient_sex:
            limit= self.path.split('=')[1]
            if limit=='':
                limit=10
            events=self.get_events(str(limit))
            events=events['results']
            patientsex=self.get_patientsex(events)
            html=self.get_patientsex_html(patientsex)
            self.wfile.write(bytes(html,'utf8'))

        return
