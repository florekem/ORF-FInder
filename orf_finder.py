"""
# Groupby groups consecutive items together based on some user-specified characteristic.
# Each element in the resulting iterator is a tuple,
# where the first element is the "key", which is a label for that group.
# The second element is an iterator over the items in that group.

# print(faiter_s.__next__())  ## to to samo co print(next(faiter_s))
# wystarczyl jeden iterator, zeby zwrocic wszystkie elementy z yield o obu przypadkach



# return bo zwracasz cala funcje, otrzymujesz dwie oddzielne listy, bo funkcja jest wywoływana dwa razy [pierwsza], [druga]
# yield bo zwracasz iterator. kiedy zwraca funcje, nie iterator, funkcja wywowyla jest raz i otrzymujesz dwie listy w liscie [[pierwsza], [druga]]
# tutaj lepiej jak listy beda oddzielne
"""


from itertools import groupby
import numpy as np

def reverse_complement(sequence):
    table = sequence.maketrans('ACGT', 'TGCA')
    
    st1 = sequence.translate(table)  #complement
    
    st1 = st1[::-1]  #reverse complement
    
    return st1
    

def faiter(file):
    """
    funkcja zwraca generator. kazdy loop generatora zawiera header oraz połączoną z poj. linii sekwencję.
    sekwencja grupowana jest do headera za pomocą groupby().
    """
    
    fh = open(file)
    
    for group, group_items_iter in groupby(fh, lambda line: line[0] == ">"):       
        header_seq_joined = "".join(group_items_iter)       
        yield header_seq_joined
 
def single_sequence(faiter_output):
    """
    funkcja zwraca pojedyncza sekwencję wraz z jej headerem w oddzielnych zmiennych
    """

    header = faiter_output.__next__().replace('\n', '')
    sequence = faiter_output.__next__().replace('\n', '')

    return (header, sequence)

def choose_frame(sequence):
    """
    zanim zdecydujesz czy sekwencja ma orf, najpierw wybierz odpowiednią (kolejną) ramkę odczytu.
    +1 (normalna, od początku), +2 (z pominieciem pierwszej zasady w sekwencji, +3 (z pominięciem dwóch
    pierwszych zasad) oraz -1,-2,-3 (jak poprzednio, ale na sekwencji reverse complement).
    """
    
    plus_one = sequence
    plus_two = sequence[1:]
    plus_three = sequence[2:]
        
    reverse_compl_sequence = reverse_complement(sequence)
        
    minus_one = reverse_compl_sequence
    minus_two = reverse_compl_sequence[1:]
    minus_three = reverse_compl_sequence[2:]
        
        
    frames_list = [plus_one, plus_two, plus_three, minus_one, minus_two, minus_three]
        
    for select_frame in frames_list:
        
        yield select_frame

def find_orfs(framed_sequence):
    """
    sprawdza, czy kodony sa sekwencjami STOP. jeśli tak, dodaj numery nukleotydów początkowych i końcowych
    kodonu stop do oddzielnych list i na ich podstawie oblicz dlugosc ORF. orf_len jest lista, która
    zawiera dlugosci wszystkich znalezionych orf.
    """
    orf_len = []
    
    # musi byc loop, ktory zbierze wyszystkie sekwencje 

    for frame in framed_sequence:
        step = 0
        stop_codons = []
        stop_codon_first_nucl_no = []
        stop_codon_last_nucl_no = []            
            
        for nucl in range(len(frame)):  #zastapic wydajniejsza licza, dlugosc calej sekwencji jest za duza
            codon = frame[step:3+step]
            step += 3
            if codon == "TAA" or codon == "TAG" or codon == "TGA":
                stop_codons.append(codon)
                stop_codon_first_nucl_no.append(step-3)
                stop_codon_last_nucl_no.append(step)
                    
        for z in range(len(stop_codon_last_nucl_no) - 1):    
            orf_len.append(stop_codon_last_nucl_no[1+z] - stop_codon_first_nucl_no[0+z])            
    
    
    return orf_len
    
def decide(orf_len):
    """
    z listy dlugosci znalezionych orf sprawdz, czy ktorys ma odpowiednia dlugosc i zdecyduj czy sekwencja jest
    kodująca czy niekodująca.
    """
    
    if not orf_len:    #jesli lista jest pusta
        decision = 'noncoding'        
    else:
        if max(orf_len) < 200 or not orf_len:
            decision = 'noncoding'
        else:
            decision = 'coding'

    if decision == 'coding':  # TYMCZASOWO, ma byc NONCODING
        return decision  # moge je tu zwracac, bo te zmienne istnieja w loopie w __main__
    else:
        pass

def check_no_of_sequences(file):
    sequences_count = 0
    f = open(file)

    for line in f:
        if line.startswith(">"):
            sequences_count += 1
    return sequences_count


"""
sekwencje przed paddowaniem, najpierw trzeba one-hot encodowac, zeby bylo co padowac, bo tak to padowac string to
"""

def one_hot(sequence):
    A = np.array(0,0,0,1)
    G = np.array(0,0.1,0)
    C = np.array(0,1,0,0)
    T = np.array(1,0,0,0)

    for nucleotide in sequnce:
        if nucleotide = 'A':
            one_hot_sequence.append() # nie do konca, bo to bedzie np array. dowiedziec sie jak modyfikowac np.array'e

    return

if __name__ == "__main__":
    examined_file = 'gfap.fasta'
    faiter_output = faiter(examined_file)
    no_of_sequences = check_no_of_sequences(examined_file)
    print(no_of_sequences)

    for i in range(no_of_sequences):
        header, sequence = single_sequence(faiter_output)
        framed_sequence = choose_frame(sequence)
        orf_len = find_orfs(framed_sequence)
        decision = decide(orf_len)

        if decision == 'coding':
            one_hot_sequence = one_hot(sequence)
            

