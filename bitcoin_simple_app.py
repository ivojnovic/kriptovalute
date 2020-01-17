from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
import requests
import tkinter as tk
from PIL import ImageTk, Image
from decimal import Decimal

def mjenjacnica():
    TICKER_API_URL = 'https://api.coinmarketcap.com/v1/ticker/'
    response = requests.get(TICKER_API_URL+'bitcoin')
    response_json = response.json()
    return Decimal(response_json[0]['price_usd'])

def on_spinbox_change():
    print("value:", spin.get())
    broj_blokova = spin.get()
    print ("broj_blokova je " + broj_blokova)
    popuni_vrijednosti(int(broj_blokova))

def popuni_vrijednosti(broj_blokova):
    blockchain = client.getblockchaininfo()
    zadnji_blok = blockchain['blocks']
    broj_transakcija_ukupno = 0
    if(broj_blokova>=0):
        blok_1.set(0)
        blok_2.set(0)
        blok_3.set(0)
        blok_4.set(0)
        blok_5.set(0)
        blok_1_broj_transakcija.set(0)
        blok_2_broj_transakcija.set(0)
        blok_3_broj_transakcija.set(0)
        blok_4_broj_transakcija.set(0)
        blok_5_broj_transakcija.set(0)
    if(broj_blokova>=1):
        blok_1.set(zadnji_blok)
        zadnji_blok_hash = client.getblockhash(zadnji_blok)
        zadnji_blok_k = client.getblock(zadnji_blok_hash)
        blok_1_broj_transakcija.set(zadnji_blok_k['nTx'])
        # for i in range(zadnji_blok_k['nTx']):
        # lista_transakcija = zadnji_blok_k['tx']
        # t = client.getrawtransaction(lista_transakcija[1], 1, zadnji_blok_hash)
        # suma = 0
        # for i in range(len(lista_transakcija)):
        #     t = client.getrawtransaction(lista_transakcija[i], 1, zadnji_blok_hash)
        #     vout = t['vout']
        #     suma+=(vout[0]['value'])
        # ukupno_BTC.set(suma)
        broj_transakcija_ukupno+=zadnji_blok_k['nTx']
    if(broj_blokova>=2):
        blok_2.set(zadnji_blok-1)
        zadnji_blok_hash = client.getblockhash(zadnji_blok-1)
        zadnji_blok_k = client.getblock(zadnji_blok_hash)
        blok_2_broj_transakcija.set(zadnji_blok_k['nTx'])
        broj_transakcija_ukupno+=zadnji_blok_k['nTx']
    if(broj_blokova>=3):
        blok_3.set(zadnji_blok-2)
        zadnji_blok_hash = client.getblockhash(zadnji_blok-2)
        zadnji_blok_k = client.getblock(zadnji_blok_hash)
        blok_3_broj_transakcija.set(zadnji_blok_k['nTx'])
        broj_transakcija_ukupno+=zadnji_blok_k['nTx']
    if(broj_blokova>=4):
        blok_4.set(zadnji_blok-3)
        zadnji_blok_hash = client.getblockhash(zadnji_blok-3)
        zadnji_blok_k = client.getblock(zadnji_blok_hash)
        blok_4_broj_transakcija.set(zadnji_blok_k['nTx'])
        broj_transakcija_ukupno+=zadnji_blok_k['nTx']
    if(broj_blokova==5):
        blok_5.set(zadnji_blok-4)
        zadnji_blok_hash = client.getblockhash(zadnji_blok-4)
        zadnji_blok_k = client.getblock(zadnji_blok_hash)
        blok_5_broj_transakcija.set(zadnji_blok_k['nTx'])
        broj_transakcija_ukupno+=zadnji_blok_k['nTx']

    broj_transakcija.set(broj_transakcija_ukupno)


def ukupno_BTC_fee_mempool():
    mempool = client.getrawmempool(True)
    ukupno_comm = 0
    min_fee = 100
    max_fee = 0
    avg_fee = 0
    i=0
    for _, value in mempool.items():
        ukupno_comm += value['fees']['base']
        i+=1
        if(value['fees']['base']<min_fee):
            min_fee = value['fees']['base']
        if(value['fees']['base']>max_fee):
            max_fee = value['fees']['base']
    avg_fee = ukupno_comm/i
    return(round(ukupno_comm,10), round(min_fee,10), round(max_fee,10), round(avg_fee,10))
client = AuthServiceProxy("http://%s:%s@blockchain.oss.unist.hr:8332"%('student', 'WYVyF5DTERJASAiIiYGg4UkRH'))
ukupno_comm_f, min_fee_f, max_fee_f, avg_fee_f = ukupno_BTC_fee_mempool()
root = tk.Tk()

root.title("Statistički pregled blokova")
root.geometry('800x800')

img = ImageTk.PhotoImage(Image.open("logo.png"))
panel = tk.Label(root, image = img, width=100, height=100)
panel.grid(row=0, column = 0, columnspan=2, rowspan=2, padx=30, sticky=tk.W)
#Spin box za ubaciti broj blokova
tk.Label(root,text="Broj zadnjih blokova za izračun").grid(row = 2, column=0, padx=25, pady=10)
spin = tk.Spinbox(root, state='readonly', values=(0, 1, 2, 3, 4, 5), bg="red", command=on_spinbox_change, width=30)
spin.grid(row = 3, column=0, padx=30, sticky=tk.W)

tk.Label(root, text="Blok", width=20, anchor=tk.W).grid(row=2,column=1,padx=25, pady=10)
tk.Label(root, text="Broj transakcija u bloku", width=20, anchor=tk.W).grid(row=2,column=2)

#Labela za 1.blok
blok_1 = tk.IntVar(root)
blok_1_labela = tk.Label(root, textvariable=blok_1, borderwidth=2, relief="solid", width=20, anchor=tk.E)
blok_1_labela.grid(row = 3, column=1, padx=30, sticky=tk.W)

#Labela za 2.blok
blok_2 = tk.IntVar(root)
blok_2_labela = tk.Label(root, textvariable=blok_2, borderwidth=2, relief="solid", width=20, anchor=tk.E)
blok_2_labela.grid(row = 4, column=1, padx=30, sticky=tk.W)

#Labela za 3.anc
blok_3 = tk.IntVar(root)
blok_3_labela = tk.Label(root, textvariable=blok_3, borderwidth=2, relief="solid", width=20, anchor=tk.E)
blok_3_labela.grid(row = 5, column=1, padx=30, sticky=tk.W)

#Labela za 4.blok
blok_4 = tk.IntVar(root)
blok_4_labela = tk.Label(root, textvariable=blok_4, borderwidth=2, relief="solid", width=20, anchor=tk.E)
blok_4_labela.grid(row = 6, column=1, padx=30, sticky=tk.W)

#Labela za 5.blok
blok_5 = tk.IntVar(root)
blok_5_labela = tk.Label(root, textvariable=blok_5, borderwidth=2, relief="solid", width=20, anchor=tk.E)
blok_5_labela.grid(row = 7, column=1, padx=30, sticky=tk.W)

#Labela za broj transakcija u prvom bloku
blok_1_broj_transakcija = tk.IntVar(root)
blok_1_labela = tk.Label(root, textvariable=blok_1_broj_transakcija, borderwidth=2, relief="solid", width=20, anchor=tk.E)
blok_1_labela.grid(row = 3, column=2, padx=5, sticky=tk.W)

#Labela za broj transakcija u drugom bloku
blok_2_broj_transakcija = tk.IntVar(root)
blok_2_labela = tk.Label(root, textvariable=blok_2_broj_transakcija, borderwidth=2, relief="solid", width=20, anchor=tk.E)
blok_2_labela.grid(row = 4, column=2, padx=5, sticky=tk.W)

#Labela za broj transakcija u trećem bloku
blok_3_broj_transakcija = tk.IntVar(root)
blok_3_labela = tk.Label(root, textvariable=blok_3_broj_transakcija, borderwidth=2, relief="solid", width=20, anchor=tk.E)
blok_3_labela.grid(row = 5, column=2, padx=5, sticky=tk.W)

#Labela za broj transakcija u četvrtom bloku
blok_4_broj_transakcija = tk.IntVar(root)
blok_4_labela = tk.Label(root, textvariable=blok_4_broj_transakcija, borderwidth=2, relief="solid", width=20, anchor=tk.E)
blok_4_labela.grid(row = 6, column=2, padx=5, sticky=tk.W)

#Labela za broj transakcija u petom bloku
blok_5_broj_transakcija = tk.IntVar(root)
blok_5_labela = tk.Label(root, textvariable=blok_5_broj_transakcija, borderwidth=2, relief="solid", width=20, anchor=tk.E)
blok_5_labela.grid(row = 7, column=2, padx=5, sticky=tk.W)

broj_transakcija = tk.IntVar(root)
tk.Label(root, text="Ukupan broj transakcija:", relief="ridge", width="20").grid(row = 8, column=1, padx=30, pady=10, sticky=tk.E)
broj_transakcija_labela = tk.Label(root, textvariable=broj_transakcija, borderwidth=2, relief="ridge", width=20, anchor=tk.E)
broj_transakcija_labela.grid(row = 8, column=2, padx=5, sticky=tk.W)

# ukupno_BTC = tk.IntVar()
# tk.Label(root, text="\u03A3 BTC (zadnji blok):", relief="ridge", width="20", anchor=tk.W).grid(row = 9, column=0, padx=30, pady=10, sticky=tk.W)
# tk.Label(root, relief="ridge", width="10", anchor=tk.E, textvariable=ukupno_BTC).grid(row = 9, column=0, padx=30, pady=10, sticky=tk.E)

ukupno_FEE = tk.StringVar()
min_fee  = tk.StringVar()
max_fee  = tk.StringVar()
avg_fee  = tk.StringVar()

ukupno_FEE.set(ukupno_comm_f)
min_fee.set(min_fee_f)
max_fee.set(max_fee_f)
avg_fee.set(avg_fee_f)

ukupno_FEE_USD = tk.DoubleVar()
min_fee_USD  = tk.DoubleVar()
max_fee_USD  = tk.DoubleVar()
avg_fee_USD = tk.DoubleVar()

BTC_u_Dolar = mjenjacnica()
print(BTC_u_Dolar)

ukupno_FEE_USD.set(round((BTC_u_Dolar * Decimal(ukupno_comm_f)),4))
min_fee_USD.set(round((BTC_u_Dolar * Decimal(min_fee_f)),4))
max_fee_USD.set(round((BTC_u_Dolar * Decimal(max_fee_f)),4))
avg_fee_USD.set(round((BTC_u_Dolar * Decimal(avg_fee_f)),4))

print(ukupno_FEE_USD.get(), min_fee_USD.get(), max_fee_USD.get(), avg_fee_USD.get())
#Ukupno fee
tk.Label(root, text="\u03A3 Fee (BTC):", relief="ridge", width="20", anchor=tk.W).grid(row = 9, column=0, padx=30, pady=10, sticky=tk.W)
ukupno_fee_labela = tk.Label(root, relief="ridge", width="10", anchor=tk.E, textvariable=ukupno_FEE)
ukupno_fee_labela.grid(row = 9, column=0, padx=30, pady=10, sticky=tk.E)
#ukupno fee u dolarima
tk.Label(root, text="\u03A3 Fee (USD):", relief="ridge", width="30", anchor=tk.W).grid(row = 9, column=1, padx=30, pady=10, sticky=tk.W)
ukupno_fee_labela = tk.Label(root, relief="ridge", width="15", anchor=tk.W, textvariable=ukupno_FEE_USD)
ukupno_fee_labela.grid(row = 9, column=1, padx=30, pady=10, sticky=tk.E)
#minimalna fee
tk.Label(root, text="Min Fee (BTC):", relief="ridge", width="20", anchor=tk.W).grid(row = 10, column=0, padx=30, pady=10, sticky=tk.W)
min_fee_labela = tk.Label(root, relief="ridge", width="10", anchor=tk.E, textvariable=min_fee)
min_fee_labela.grid(row = 10, column=0, padx=30, pady=10, sticky=tk.E)
#min fee u USD
tk.Label(root, text="Min Fee (USD):", relief="ridge", width="30", anchor=tk.W).grid(row = 10, column=1, padx=30, pady=10, sticky=tk.W)
ukupno_fee_labela = tk.Label(root, relief="ridge", width="15", anchor=tk.W, textvariable=min_fee_USD)
ukupno_fee_labela.grid(row = 10, column=1, padx=30, pady=10, sticky=tk.E)
#max fee u BTC
tk.Label(root, text="Max Fee (BTC):", relief="ridge", width="20", anchor=tk.W).grid(row = 11, column=0, padx=30, pady=10, sticky=tk.W)
max_fee_labela = tk.Label(root, relief="ridge", width="10", anchor=tk.E, textvariable=max_fee)
max_fee_labela.grid(row = 11, column=0, padx=30, pady=10, sticky=tk.E)
#max fee u USD
tk.Label(root, text="Max Fee (USD):", relief="ridge", width="30", anchor=tk.W).grid(row = 11, column=1, padx=30, pady=10, sticky=tk.W)
ukupno_fee_labela = tk.Label(root, relief="ridge", width="15", anchor=tk.W, textvariable=max_fee_USD)
ukupno_fee_labela.grid(row = 11, column=1, padx=30, pady=10, sticky=tk.E)
#AVG fee u BTC
tk.Label(root, text="Avg Fee (BTC):", relief="ridge", width="20", anchor=tk.W).grid(row = 12, column=0, padx=30, pady=10, sticky=tk.W)
avg_fee_labela = tk.Label(root, relief="ridge", width="10", anchor=tk.E, textvariable=avg_fee)
avg_fee_labela.grid(row = 12, column=0, padx=30, pady=10, sticky=tk.E)

#avg fee u USD
tk.Label(root, text="Avg Fee (USD):", relief="ridge", width="30", anchor=tk.W).grid(row = 12, column=1, padx=30, pady=10, sticky=tk.W)
ukupno_fee_labela = tk.Label(root, relief="ridge", width="15", anchor=tk.W, textvariable=avg_fee_USD)
ukupno_fee_labela.grid(row = 12, column=1, padx=30, pady=10, sticky=tk.E)

root.mainloop()
