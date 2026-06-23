from fpdf import *
from datetime import datetime
import sqls

def formatea(tot,si=0):
	if si==1:
		snumero = str(tot)
		deci = snumero[-4:]
		entero = snumero[:-4]
	else:	
		snumero = '{:.2f}'.format(tot).replace('.',',')   
		deci = snumero[-3:]
		entero = snumero[:-3]

	formato = ''
	punto = ''
	while len(entero) > 0:
		formato =  entero[-3:] + punto + formato
		entero = entero[:-3]
		punto = '.'


	return formato + deci

def x_nulo(dato, devolver=''):
    if dato is None:
        return devolver
    else:
        return str(dato)


def padron(socios):        
        alinea = 'I'
        alto = 6
        borde = 1
        sin_borde = 0
        salto = 0
        ancho = 40
        espacio = 40
        pdf=FPDF()
            
        pdf.add_page()
        pdf.set_font('Arial','B',12)

        #def cell(self, w,h=0,txt='',border=0,ln=0,align='',fill=0,link=''):
        pdf.cell(1250,alto,'                                                      CLUB JAPONES LA PLATA',border=sin_borde,align='L')
        pdf.ln(12)
        pdf.set_font('Arial','B',12)
        pdf.cell(1250,alto,'                                                                 Padron',sin_borde,salto,'I')
        pdf.ln(3)
        pdf.cell(200,alto,'__________________________________________________________________________________',sin_borde,salto,'I')

        grupo_ant = -1
        
        for socio in socios:
            grupo = socio[0]
            nombre = socio[1]
            parentesco = sqls.sparentesco(socio[2])
            fecNac = socio[3]
            sfecNac = fecNac.strftime("%d-%m-%Y")
            domicilio = socio[4]

            if grupo != grupo_ant:
                pdf.ln(8)    
                pdf.set_font('Arial','B',12)
                pdf.cell(ancho,6,'Grupo : '  + str(grupo),0, salto)
                #pdf.cell(ancho,6, str(grupo), 0, align='C')
                pdf.ln(10)    
                grupo_ant = grupo
        
            pdf.set_font('Arial','',10)
            pdf.cell(ancho,6, nombre, 0, align='C')
            pdf.cell(ancho,6, str(parentesco), 0, align='C')
            pdf.cell(ancho,6, str(sfecNac), 0, align='C')
            pdf.cell(ancho,6, domicilio, 0, align='C')
            pdf.ln(5)    
        
        return pdf.output(dest='S').encode('latin-1')

def porJubilarse(socios):        
        alinea = 'I'
        alto = 6
        borde = 1
        sin_borde = 0
        salto = 0
        ancho = 37
        espacio = 40
        pdf=FPDF()
            
        pdf.add_page()
        pdf.set_font('Arial','B',12)

        #def cell(self, w,h=0,txt='',border=0,ln=0,align='',fill=0,link=''):
        pdf.cell(1250,alto,'                                                                CLUB JAPONES LA PLATA',border=sin_borde,align='L')
        pdf.ln(12)
        pdf.set_font('Arial','B',12)
        pdf.cell(1250,alto,'                                                                 Socios por Jubilarse',sin_borde,salto,'I')
        pdf.ln(13)
        pdf.set_font('Arial','B',10)
        pdf.cell(ancho,6, 'Grupo', 0, align='C')
        pdf.cell(ancho,6, 'Nombre', 0, align='C')
        pdf.cell(ancho,6, 'Parentesco', 0, align='C')
        pdf.cell(ancho,6, 'Edad', 0, align='C')
        pdf.cell(ancho,6, 'Domicilio', 0, align='C')
        pdf.ln(2)    
        pdf.cell(200,alto,'____________________________________________________________________________________________',sin_borde,salto,'I')
        pdf.ln(10)
        pdf.set_font('Arial','',10)

        for socio in socios:
            grupo = socio[0]
            nombre = socio[1]
            parentesco = sqls.sparentesco(socio[2])
            edad = socio[3]
            domicilio = socio[4]

            pdf.cell(ancho,6, str(grupo), 0, align='C')
            pdf.cell(ancho,6, nombre, 0, align='C')
            pdf.cell(ancho,6, str(parentesco), 0, align='C')
            pdf.cell(ancho,6, str(edad), 0, align='C')
            pdf.cell(ancho,6, domicilio, 0, align='C')
            pdf.ln(5)    
        
        return pdf.output(dest='S').encode('latin-1')
    
if __name__ == '__main__':
    #engine = create_engine('postgresql+psycopg2://postgres:pablo@localhost:5432/presidencia')
    
    engine = sqls.coneccion()
    SessionX = sessionmaker(bind=engine)
    db = SessionX()


    p=generar(db, 139,2021,[] ,'CPI')    
    #p=generar(db, 841,2018)    
    
    #generar(db, 1,2019)    