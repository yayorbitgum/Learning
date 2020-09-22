# http://rosalind.info/problems/dna/


# Counting DNA Nucleotides

DNAFile = open("rosalind_dna.txt")
DNASequence = DNAFile.read()        # Read the file, assign it to variable

countA = DNASequence.count('A')    # Assign each count to variable
countC = DNASequence.count('C')
countG = DNASequence.count('G')
countT = DNASequence.count('T')

Counts = (countA, countC, countG, countT)    # Put counts into specific order


print("////////////////// Problem 1: Counting DNA Nucleotides ////////////////")
print("Nucleotide amounts:")


def print_dncount_as(letter):         # Matches and prints letters with counts
	if letter == 'A':
		print(letter + ": %d" % Counts[0])
	elif letter == 'C':
		print(letter + ": %d" % Counts[1])
	elif letter == 'G':
		print(letter + ": %d" % Counts[2])
	elif letter == 'T':
		print(letter + ": %d" % Counts[3])


DNANucleotides = ('A', 'C', 'G', 'T')    # Tuple of possible letters for the loop

for letters in DNANucleotides:         # Loop through above tuple and
	print_dncount_as(letters)          # Run above function for each letter

print("////////////////// Solution format ////////////////")
print(f"{Counts[0]}, {Counts[1]}, {Counts[2]}, {Counts[3]}")

# Solved successfully!


# http://rosalind.info/problems/rna/
# Transcribing DNA to RNA

DNAFile = open("rosalind_rna.txt")
DNASequence = DNAFile.read()
RNATranscribe = DNASequence.replace('T', 'U')

print("////////////////// Problem 2: RNA Transcribe ////////////////")
print(RNATranscribe)

# Solved successfully!


# http://rosalind.info/problems/revc/
# Complementing a Strand of DNA
#
# By complementarity, once we know the order of bases on one strand, 
# we can immediately deduce the sequence of bases in the complementary strand. 
# These bases will run in the opposite order to match the fact that the two 
# strands of DNA run in opposite directions.
#
# In DNA strings, symbols 'A' and 'T' are complements of each other, 
# as are 'C' and 'G'.
# The reverse complement of a DNA string s is the string sc formed by reversing 
# the symbols of s, then taking the complement of each symbol 
# (e.g., the reverse complement of "GTCA" is "TGAC").

# Will need to change between upper and lower case so they don't overwrite twice


DNAFile = open("rosalind_revc.txt")
DNASequence = DNAFile.read()

DNASeqLower = DNASequence.replace('A', 'a')    # <- Swap to new variable here
DNASeqLower = DNASeqLower.replace('C', 'c')    # <- Continue to update new variable
DNASeqLower = DNASeqLower.replace('G', 'g')
DNASeqLower = DNASeqLower.replace('T', 't')

DNAReverseLower = DNASeqLower[::-1]   # [start : end : step amount and direction]

DNAComplement = DNAReverseLower.replace('a', 'T')
DNAComplement = DNAComplement.replace('c', 'G')
DNAComplement = DNAComplement.replace('g', 'C')
DNAComplement = DNAComplement.replace('t', 'A')

print("////////////////// Problem 3: Reverse Complement ////////////////")
print(DNAComplement)

# Solved successfully!

