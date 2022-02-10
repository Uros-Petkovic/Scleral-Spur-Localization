# -*- coding: utf-8 -*-
"""
Created on Sun May 17 17:13:52 2020

@author: pu160186d and ak160180d
"""

# Importujemo potrebne biblioteke
import imageio
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndi

# Koristimo dva for ciklusa za citanje svih slika iz dataseta
# Broj1 predstavlja broj slike pre crtice
# Broj2 predstavlja broj slike posle crtice
# Date slike se nalaze u formatu "T0XXX-XX.jpg"
# Slike medjukoraka su zakomentarisane kako ne bi punile memoriju
# Pokazuju se samo ulazne i konacne slike, uz ovaj kod prilozen je jos jedan kod
# u kome je moguce pojedinacno pokretanje slika sa svim medjukoracima

for p1 in range(1,21):
    for p2 in range(1,17):
        broj1=str(p1); #Prebacujemo dati broj u string
        broj2=str(p2); #Prebacujemo dati broj u string
        
        # Vrsimo konkatenaciju radi dobijanja konacnog naziva slike
        slika="T0"+ broj1.rjust(3,'0')+"-"+broj2.rjust(2,'0')+".jpg";
        # Naziv predstavlja konacnu putanju do slike
        naziv="D:/FAKS-UROS/CETVRTA GODINA/ABS/ABS Projekat/Nasdataset/" + slika;
        #Ucitavamo ulaznu sliku na kojoj treba lokalizovati scleral spur
        img=imageio.imread(naziv);
        # Prikazujemo originalnu sliku
        plt.figure();
        plt.imshow(img);
        plt.title('Ulazna slika');
        plt.xlabel('x koordinata');
        plt.ylabel('y koordinata');
        
        # Uporedjujemo RGB plejnove
        #plt.figure();
        #plt.imshow(img[:,:,0],cmap='gray');
        #plt.title('Izdvajanje R komponente');
        #plt.xlabel('x koordinata');
        #plt.ylabel('y koordinata');
        #plt.figure();
        #plt.imshow(img[:,:,1],cmap='gray');
        #plt.figure();
        #plt.imshow(img[:,:,2],cmap='gray');
        
        # Kao posmatrani plejn uzimamo R plejn usled pojave
        # plavog suma na originalnoj slici
        img=img[:,:,0];
        # Pravimo masku za mean filtar radi uklanjanja Gausovog suma
        n=3;
        mask=np.zeros(shape=(n,n))+1/(n*n);
        img1=ndi.convolve(img,mask); #Vrismo usrednjavanje slike
        # Prikazujemo dobijenu sliku posle mean filtra
        #plt.figure();
        #plt.imshow(img1,cmap='gray');
        #plt.title('Slika nakon mean filtra');
        #plt.xlabel('x koordinata');
        #plt.ylabel('y koordinata');
        
        # Vrsimo uklanjanje impulsnog suma medijan filtrom i prikazujemo rezultat
        img2=ndi.median_filter(img,(11,11));
        img2=ndi.convolve(img2,mask);
        #plt.figure();
        #plt.imshow(img2,cmap='gray');
        #plt.title('Slika nakon median filtra');
        #plt.xlabel('x koordinata');
        #plt.ylabel('y koordinata');
         
        # Vrsimo poredjenje sa pragom kako bismo binarizovali sliku
        img2=img2>17;
        # Vrsimo ponovno filtriranje medijan filtrom
        # kako bismo potisnuli impulsni sum na binarizovanoj slici
        img2=ndi.median_filter(img2,(7,7));
        
        #plt.figure(); # Prikazujemo sliku
        #plt.imshow(img2,cmap='gray');
        #plt.title('Slika nakon poredjenja sa pragom');
        #plt.xlabel('x koordinata');
        #plt.ylabel('y koordinata');
        
        img2=ndi.median_filter(img2,(9,9));
        # Ponovno usrednjavamo sliku radi suzbijanja belih tacaka
        # koje narusavaju kvalitet segmentacije
        n=5;
        maska=np.zeros(shape=(n,n))+1/(n*n);
        img3=ndi.convolve(img2,maska);
        # Vrsimo dilataciju pre pocetka same segmentacije
        img3=ndi.binary_dilation(img3,iterations=12);
        #plt.figure();
        #plt.imshow(img3,cmap='gray');
        #plt.title('Slika nakon dilatacije');
        #plt.xlabel('x koordinata');
        #plt.ylabel('y koordinata');
        
        # Vrsimo eventualno potrebno odsecanje slike sa donje strane
        # kako bi razdvojili potrebne label-ove pri segmentaciji
        # posto problem stvaraju slike koje imaju previse crnog segmenta
        # u donjem delu slike
        # Zbog slika koje mogu biti blago zarotirane na obe strane
        # radimo odvojeno odsecanje slike za levi i desni segment
        # i dobijamo potrebne granice za odsecanje za levi i desni
        # scleral spur do kojih cemo posmatrati sliku pri lokalizaciji
        for i in range (997,-1,-1):
            if (img3[i,0:770].sum()>350):    
                break
        granica1=i;
        # Posmatramo pribliznih 36% na pocetku i poslednjih 36% na kraju slike
        # po horizontalnoj osi zbog nuspojava na slikama koje se javljaju u sredinjsem 
        # delu koje nisu od interesa pri segmentaciji, a kvare njeno odredjivanje
        for i in range (997,-1,-1):
            if (img3[i,1400:2129].sum()>350):    
                break
        granica2=i;

        # U daljoj obradi koristimo slike koje su ogranicene datim granicama
        # po y-osi i prikazujemo date slike
        img31=img3[0:granica1,:];
        img32=img3[0:granica2,:];
        #plt.figure();
        #plt.imshow(img31);
        #plt.title('Prikaz odsecanja do leve granice');
        #plt.xlabel('x koordinata');
        #plt.ylabel('y koordinata');
        
        #plt.figure();
        #plt.imshow(img32); 
        #plt.title('Prikaz odsecanja do desne granice');
        #plt.xlabel('x koordinata');
        #plt.ylabel('y koordinata');
        
        # Radi segmentisanja potrebnih oblasti vrsimo negativ slike
        img41=1-img31;
        img42=1-img32;
        # Nalazimo trazene oblasti za levi i desni segment
        img51=ndi.label(img41);
        #plt.figure(); # Prikazujemo oblast za levi deo
        #plt.imshow(img51[0]);
        #plt.title('Pronalazenje izdvojenih segmenata leve strane');
        #plt.xlabel('x koordinata');
        #plt.ylabel('y koordinata');

        img52=ndi.label(img42);
        #plt.figure(); #Prikazujemo oblast za desni segment
        #plt.imshow(img52[0]);
        #plt.title('Pronalazenje izdvojenih segmenata desne strane');
        #plt.xlabel('x koordinata');
        #plt.ylabel('y koordinata');

        # Na segmentisanoj slici za segment od interesa
        # koji predstavlja segmentisanu prednju ocnu komoru
        # trazimo krajnju levu tacku, odnosno minimalnu tacku
        # po horizontalnoj osi koja se javlja usled ostrog ugla izmedju
        # roznjace i duzice
        img8=np.empty((granica1,2130));
        for i in range(0,granica1):
            for j in range (0,2130):
                if (img51[0][i,j]==img51[0][granica1-250,770]):
                    img8[i,j]=j;
                else:
                    img8[i,j]=2400;
     
        # Prikazujemo segmentisanu oblast
        # na kojoj se vidi porast horizontalne koordinate
                    
        #plt.figure(); 
        #plt.imshow(img8);
        #plt.title('Prikaz leve regije od interesa u rastucem poretku');
        #plt.xlabel('x koordinata');
        #plt.ylabel('y koordinata');
                    
        # Trazenje krajnje leve tacke svodi se na nalazenje
        # minimuma horizontalne koordinate dok sve ostale tacke
        # van posmatranog segmenta stavljamo na vrednost 2400 kako
        # bismo sa sigurnoscu znali da one nece biti minimum
        x1=int(img8.min());
        # Lokalizacija levog scleral spura
        for i in range(0,granica1):
            if (img8[i,x1]!=2400):
                break
        
        y1=i;
        x1=x1-10;
        y1=y1+10;         
        
        # Isto radimo i za desni segment, samo sto lokalizujemo
        # krajnju desnu tacku, odnosno njen maksimum po horizontalnoj
        # koordinati, a tacke van posmatrane oblasti postavljamo na nulu
        img9=np.empty((granica2,2130));
        for i in range(0,granica2):
            for j in range (0,2130):
                if (img52[0][i,j]==img52[0][granica2-248,1400]):
                    img9[i,j]=j;
                else:
                    img9[i,j]=0;

        #plt.figure(); # Prikazivanje
        #plt.imshow(img9);
        #plt.title('Prikaz desne regije od interesa u rastucem poretku');
        #plt.xlabel('x koordinata');
        #plt.ylabel('y koordinata');

        # Nalazenje maksimuma    
        x2=int(img9.max());

        for i in range(0,granica2):
            if (img9[i,x2]!=0):
                break
        y2=i;
        x2=x2+10;
        y2=y2+10; 
        
        # Prikazivanje levog i desnog lokalizovanog scleral spura
        plt.figure();
        #fig=plt.figure(figsize=(9.98,21.30)); #Ovo ako hocemo da cuvamo slike
        plt.imshow(img,cmap='gray');
        plt.scatter(x2,y2,marker="x",c="red",s=20); 
        plt.scatter(x1,y1,marker="x",c="red",s=20);
        plt.title('Prikaz lokalizovanih scleral spursa');
        plt.xlabel('x koordinata');
        plt.ylabel('y koordinata'); 
        #fig.savefig(slika); #Ovo ako hocemo da cuvamo slike