produse = ["espresso", "latte", "cappuccino", "ceai", "ciocolata calda", "croissant"]
preturi = [8.0, 12.0, 11.0, 7.0, 10.0, 9.0]
stoc = [20, 15, 18, 30, 12, 10]
cant_comanda = [0, 0, 0, 0, 0, 0]
reducere_curenta = 0.0
tip_reducere_activa = "fara"

def afisare_meniu_produse(produse, preturi, stoc):
    print("\n--- MENIU PRODUSE ---")
    print(f"{'ID':<4} {'Produs':<18} {'Pret':<8} {'Stoc':<5}")
    for i in range(len(produse)):
        print(f"{i:<4} {produse[i]:<18} {preturi[i]:<8.2f} {stoc[i]:<5}")

def adaugare_produs(cant_comanda, stoc, index, cantitate):
    if 0 <= index < len(produse):
        if cantitate > 0:
            if cant_comanda[index] + cantitate <= stoc[index]:
                cant_comanda[index] += cantitate
                print(f"Succes: Am adaugat {cantitate} x {produse[index]}.")
                return True
            else:
                print(f"Eroare: Stoc insuficient! Disponibil: {stoc[index] - cant_comanda[index]}")
        else:
            print("Eroare: Cantitatea trebuie sa fie pozitiva.")
    else:
        print("Eroare: Index invalid.")
    return False

def scadere_produs(cant_comanda, index, cantitate):
    if 0 <= index < len(produse):
        if cantitate > 0:
            if cant_comanda[index] >= cantitate:
                cant_comanda[index] -= cantitate
                print(f"Succes: Am eliminat {cantitate} x {produse[index]}.")
                return True
            else:
                print("Eroare: Nu poti scadea mai mult decat ai in comanda.")
        else:
            print("Eroare: Cantitatea trebuie sa fie pozitiva.")
    else:
        print("Eroare: Index invalid.")
    return False

def calcul_total(cant_comanda, preturi):
    total = 0.0
    for i in range(len(cant_comanda)):
        total += cant_comanda[i] * preturi[i]
    return total

def stabilire_reducere(total, tip):
    if total <= 0: return 0.0

    valoare = 0.0
    if tip == "student":
        if total >= 30.0:
            valoare = 0.10 * total
        else:
            print("Total insuficient pentru student (minim 30.00 lei).")
    elif tip == "happy":
        if total >= 50.0:
            valoare = 0.15 * total
        else:
            print("Total insuficient pentru happy (minim 50.00 lei).")
    elif tip == "cupon":
        if total >= 25.0:
            valoare = 7.0
        else:
            print("Total insuficient pentru cupon (minim 25.00 lei).")

    # Protectie total negativ
    if valoare > total:
        valoare = total
    return valoare

def afisare_bon(cant_comanda, produse, preturi, reducere):
    total_brut = calcul_total(cant_comanda, preturi)
    print("\n========= BON FISCAL =========")
    for i in range(len(cant_comanda)):
        if cant_comanda[i] > 0:
            subtotal = cant_comanda[i] * preturi[i]
            print(f"{produse[i]:<15} {cant_comanda[i]} x {preturi[i]:>5.2f} = {subtotal:>6.2f} lei")
    print("-" * 30)
    print(f"Total Brut:          {total_brut:>6.2f} lei")
    print(f"Reducere:           -{reducere:>6.2f} lei")
    print(f"TOTAL FINAL:         {max(0, total_brut - reducere):>6.2f} lei")
    print("==============================\n")

def finalizare_comanda(stoc, cant_comanda):
    for i in range(len(cant_comanda)):
        stoc[i] -= cant_comanda[i]
        cant_comanda[i] = 0

def anulare_comanda(cant_comanda):
    for i in range(len(cant_comanda)):
        cant_comanda[i] = 0

while True:
    print("\n=== CAFENEA - MENIU PRINCIPAL ===")
    print("1. Afisare produse")
    print("2. Adaugare in comanda")
    print("3. Scadere din comanda")
    print("4. Aplicare reducere")
    print("5. Finalizare comanda (Bon)")
    print("6. Anulare comanda")
    print("0. Iesire")

    optiune = input("Alege optiunea: ")

    if optiune == "1":
        afisare_meniu_produse(produse, preturi, stoc)

    elif optiune == "2":
        try:
            idx = int(input("Index produs: "))
            cant = int(input("Cantitate: "))
            adaugare_produs(cant_comanda, stoc, idx, cant)
        except ValueError:
            print("Eroare: Te rugam sa introduci numere intregi.")

    elif optiune == "3":
        try:
            idx = int(input("Index produs: "))
            cant = int(input("Cantitate de scazut: "))
            scadere_produs(cant_comanda, idx, cant)
        except ValueError:
            print("Eroare: Te rugam sa introduci numere intregi.")

    elif optiune == "4":
        total_acum = calcul_total(cant_comanda, preturi)
        if total_acum == 0:
            print("Comanda este goala. Nu se poate aplica reducerea.")
        else:
            print(f"\nSub-meniu Reduceri (Total curent: {total_acum:.2f} lei)")
            print("a. Student (10% la total >= 30)")
            print("b. Happy (15% la total >= 50)")
            print("c. Cupon (-7 lei la total >= 25)")
            print("d. Fara reducere")
            print("e. Inapoi")
            sub_opt = input("Alege: ").lower()

            if sub_opt == "a":
                tip_reducere_activa = "student"
                reducere_curenta = stabilire_reducere(total_acum, "student")
            elif sub_opt == "b":
                tip_reducere_activa = "happy"
                reducere_curenta = stabilire_reducere(total_acum, "happy")
            elif sub_opt == "c":
                tip_reducere_activa = "cupon"
                reducere_curenta = stabilire_reducere(total_acum, "cupon")
            elif sub_opt == "d":
                tip_reducere_activa = "fara"
                reducere_curenta = 0.0
                print("Reducerea a fost resetata.")
            elif sub_opt == "e":
                print("Revenire in meniul principal.")

    elif optiune == "5":
        total_f = calcul_total(cant_comanda, preturi)
        if total_f == 0:
            print("Nu exista produse in comanda.")
        else:
            # Recalculare reducere inainte de bon (pentru siguranta)
            reducere_fina = stabilire_reducere(total_f, tip_reducere_activa)
            afisare_bon(cant_comanda, produse, preturi, reducere_fina)
            finalizare_comanda(stoc, cant_comanda)
            reducere_curenta = 0.0
            tip_reducere_activa = "fara"
            print("Comanda a fost finalizata cu succes!")

    elif optiune == "6":
        anulare_comanda(cant_comanda)
        reducere_curenta = 0.0
        tip_reducere_activa = "fara"
        print("Comanda a fost anulata.")

    elif optiune == "0":
        print("La revedere!")
        break
    else:
        print("Optiune invalida.")