# -*- coding: utf-8 -*-
"""A11-S10.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Rdme493Cj7IbslsB-T8mnrNNcSvB97tx

# Α. Στοιχεία Ομάδας
***
***

|Όνομα|ΑΜ|Ομάδα|
|-|-|-|
|Λιάτσος Γεώργιος-Ελευθέριος|03114026|Α11|
|Κουτρούλης Σπυραντώνης     |03114864|Α11|
"""

!pip install --upgrade pip #upgrade pip package installer
!pip install scikit-learn --upgrade #upgrade scikit-learn package
!pip install numpy --upgrade #upgrade numpy package
!pip install pandas --upgrade #upgrade pandas package
!pip install -U imbalanced-learn #upgrade imbalanced-learn package

"""***
***
# Β. Εισαγωγή του dataset
***
***

### B1. Παρουσίαση του dataset
 Τα δεδομένα αποτελούν στοιχεία της σιλουέτας 4 αυτοκινήτων(van,saab,opel,bus) τα οποία εθεάθησαν απο διάφορες γωνίες για να γίνουν οι απαραίτητες μετρήσεις

#### Διάβασμα των αρχείων και δημιουργία του πίνακα με τα δεδομένα
"""

import pandas as pd
import numpy as np

A = ['a','b','c','d','e','f','g','h','i']
a = []
for i in A:
    a.append(pd.read_table("https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/vehicle/xa"+ '{}'.format(i) + ".dat",header=None,delim_whitespace=True))
    
x = pd.concat([a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8]])
x.shape

"""### B2. Δείγματα και χαρακτηριστικά 

 Το μέγεθος του dataset το βρήκαμε απο πάνω. Οπότε ο αριθμός των δειγμάτων είναι 846 και ο αριθμός των χαρακτηριστικών είναι 18 + 1 της κλάσης.

 Τα χαρακτηριστικά αναγράφονται στο αρχείο "vehicle.doc" στον ίδιο φάκελο με τα αρχεία data και είναι τα εξής : 
 
    1.COMPACTNESS (average perim)**2/area
	2.CIRCULARITY (average radius)**2/area
	3.CIRCULARITY area/(av.distance from border)**2
	4.RATIO (max.rad-min.rad)/av.radius
	5.PR.AXIS ASPECT RATIO (minor axis)/(major axis)
	6.MAX.LENGTH ASPECT RATIO	(length perp. max length)/(max length)
	7.SCATTER RATIO (inertia about minor axis)/(inertia about major axis)
	8.ELONGATEDNESS area/(shrink width)**2
	9.PR.AXIS RECTANGULARITY	area/(pr.axis length*pr.axis width)
    10.MAX.LENGTH RECTANGULARITY area/(max.length*length perp. to this)
    11.SCALED VARIANCE ALONG MAJOR AXIS (2nd order moment about minor axis)/area
	12.SCALED VARIANCE ALONG MINOR AXIS (2nd order moment about major axis)/area
	13.SCALED RADIUS OF GYRATION (mavar+mivar)/area
	14.SKEWNESS ABOUT MAJOR AXIS (3rd order moment about major axis)/sigma_min**3
	15.SKEWNESS ABOUT MINOR AXIS (3rd order moment about minor axis)/sigma_maj**3
	16.ABOUT MINOR AXIS (4th order moment about major axis)/sigma_min**4
	17.KURTOSIS ABOUT MAJOR AXIS (4th order moment about minor axis)/sigma_maj**4
	18.HOLLOWS RATIO (area of hollows)/(area of bounding polygon)
    19.CLASS
 
 #### Δεν υπάρχουν μη διατεταγμένα χαρακτηριστικά

#### Αλλαγή ονομάτων στηλών σύμφωνα με τα attributes
"""

attributes = ['COMPACTNESS','CIRCULARITY','DISTANCE CIRCULARITY','RADIUS RATIO','PR.AXIS ASPECT RATIO','MAX.LENGTH ASPECT RATIO','SCATTER RATIO','ELONGATEDNESS',
              'PR.AXIS RECTANGULARITY','MAX.LENGTH RECTANGULARITY','SCALED VARIANCE(MAJOR AXIS)','SCALED VARIETY(MINOR AXIS)','SCALED RADIUS OF GYRATION',
              'SKEWNESS(MAJOR AXIS)','SKEWNESS(MINOR AXIS)','KURTOSIS(MINOR AXIS)','KURTOSIS(MAJOR AXIS)','HOLLOWS RATIO','CLASS']
for i in range(0,19):
    x.rename(columns = {i:attributes[i]},inplace=True)
x.head()

"""### Β3. Επικεφαλίδες και αρίθμηση γραμμών

 Όταν πρωτοδιαβάσαμε το αρχείο παρατηρήσαμε πως δεν υπάρχει επικεφαλίδα οπότε με την επιλογή header=None της εντολής read_table της βιβλιοθήκης pandas εξασφαλίσαμε μια ομαλή απεικόνιση. Όσον αφορά την αρίθμηση, το αρχείο δεν περιείχε απο μόνο του οπότε αφήσαμε το pandas να κάνει τη δουλειά του indexing με τη δική του αρίθμηση.

### Β4.  Κλάσεις 

Εύκολα μπορούμε να δούμε απο πάνω πως η κολόνα class βρίσκεται στην 19η θέση και από τα χαρακτηριστικά φαίνεται πως οι ετικέτες των κλάσεων είναι 4 : van,saab,opel,bus

### Β5. Μετατροπές στα αρχεία

- header = None για να διαβάσουμε το αρχείο χωρίς επικεφαλίδα
- delim_whitespace = True γιατί διάβαζε κάποια κενά στην τελευταία στήλη επειδή αν δούμε τις κλάσεις κάποιες είναι 4 γράμματα και κάποιες 3. Οπότε έπρεπε να αγνοήσουμε τα κενά για την ομαλή συνέχεια
- Τα δεδομένα βρίσκονταν σε 8 διαφορετικά αρχεία. Αφού τα διαβάσαμε και τα κάναμε ένα ένα append σε μία κενή λίστα, κάναμε concat τα στοιχεία της λίστας για να έχουμε ένα συγκεντρωτικό dataframe
- Δημιουργήσαμε τον πίνακα με τα attributes και τον προσαρμόσαμε στο dataframe

### B6. Απουσιάζουσες τιμές
"""

x.isnull().values.any()

"""Ελέγχουμε αν υπάρχουν απουσιάζουσες τιμές. **Δεν υπάρχουν.**

### B7. Έλεγχος εξισορροπημένου dataset
"""

# Έλεγχος μονο της στήλης CLASS
y = x.loc[:,['CLASS']]

# Get dummies για τα classes μας
y = pd.get_dummies(y)

# Εύρεση ποσοστών δειγμάτων επί του συνόλου
avg = (y.T.sum(axis=1))/y.shape[0]

print(avg)

"""Παρατηρούμε λοιπόν πως το dataset **είναι εξισορροπημένο**.

### Β8. Διαχωρισμός σε train και test set (20%)
"""

from sklearn.model_selection import train_test_split

# KNN train, test set
features = np.array(x.drop(['CLASS'],1))
labels = np.array(x['CLASS'])

train, test, train_labels, test_labels = train_test_split(features,labels,test_size=0.20)

# Εύρεση αριθμού δειγμάτων κάθε κλάσης στο test set
num = y.T.sum(axis=1)
num = [num[0],num[1],num[2],num[3]]
print(num)

"""***
***
# Γ. Baseline classification
***
***

## *** Γ1. Train - Test ***

### Δήλωση συναρτήσεων

Δημιουργούμε μια συνάρτηση, την ***mets*** που θα τυπώνει και θα επιστρέφει τις f1 micro και macro για κάθε ταξινομητή, καθώς και μία άλλη συνάρτηση, την ***conmat*** που θα δημιουργεί και θα τυπώνει το confusion matrix του κάθε ταξινομητή στη μορφή που θέλουμε, καθώς και το classification report.
"""

from sklearn.metrics import f1_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report 

def mets(lbls,prds,name):
    f1_micro = f1_score(lbls,prds,average='micro')
    f1_macro = f1_score(lbls,prds,average='macro')
    print("**" + name + " AVGS**")
    print("f1 micro avg = " ,f1_micro)
    print("f1 macro avg = " ,f1_macro, "\n")
    return [f1_micro,f1_macro]
  
def conmat(lbls,prds,lb_names):
    # Compute confusion matrix
    cnf_matrix = confusion_matrix(lbls, prds)
    df = pd.DataFrame(cnf_matrix)
    df.columns = lb_names
    df['Class'] = lb_names
    df.set_index("Class",inplace=True)
     
    print(classification_report(lbls, prds, target_names=lb_names))
    return df

"""### a) Dummy

#### Dummy Metrics
"""

from sklearn.dummy import DummyClassifier
import warnings
warnings.filterwarnings("ignore")

dc_default = DummyClassifier()
dc_uniform = DummyClassifier(strategy="uniform")
dc_constant_bus = DummyClassifier(strategy="constant", constant='bus')
dc_constant_opel = DummyClassifier(strategy="constant", constant='opel')
dc_constant_saab = DummyClassifier(strategy="constant", constant='saab')
dc_constant_van = DummyClassifier(strategy="constant", constant='van')
dc_most_frequent = DummyClassifier(strategy="most_frequent")

#με τη μέθοδο fit "εκπαιδεύουμε" τον ταξινομητή στο σύνολο εκπαίδευσης (τα χαρακτηριστικά και τις ετικέτες τους)
dc_default.fit(train, train_labels)
dc_uniform.fit(train, train_labels)
dc_constant_bus.fit(train, train_labels)
dc_constant_opel.fit(train, train_labels)
dc_constant_saab.fit(train, train_labels)
dc_constant_van.fit(train, train_labels)
dc_most_frequent.fit(train, train_labels)

#με τη μέθοδο predict παράγουμε προβλέψεις για τα δεδομένα ελέγχου (είσοδος τα χαρακτηριστικά μόνο)
preds_default = dc_default.predict(test)
preds_uniform = dc_uniform.predict(test)
preds_constant_van = dc_constant_van.predict(test)
preds_constant_opel = dc_constant_opel.predict(test)
preds_constant_saab = dc_constant_saab.predict(test)
preds_constant_bus = dc_constant_bus.predict(test)
preds_most_frequent = dc_most_frequent.predict(test)

# Τυπώνουμε τα AVG με την κλήση της συνάρτησης mets
dummy_metrics_default = mets(test_labels,preds_default,"DUMMY DEFAULT")
dummy_metrics_uniform = mets(test_labels,preds_uniform,"DUMMY UNIFORM")
dummy_metrics_van = mets(test_labels,preds_constant_van,"DUMMY VAN")
dummy_metrics_opel = mets(test_labels,preds_constant_opel,"DUMMY OPEL")
dummy_metrics_saab = mets(test_labels,preds_constant_saab,"DUMMY SAAB")
dummy_metrics_bus = mets(test_labels,preds_constant_bus,"DUMMY BUS")
dummy_metrics_most_frequent = mets(test_labels,preds_most_frequent,"DUMMY MOST FREQUENT")

"""#### Dummy Confusion Matrix"""

label_names = np.array(['bus','opel','saab','van'])
print("Default Matrices\n")
default_conmat = conmat(test_labels,preds_default,label_names)
default_conmat

print("Uniform Matrices\n")
uniform_conmat = conmat(test_labels,preds_uniform,label_names)
uniform_conmat

print("Constant Bus Matrices\n")
bus_conmat = conmat(test_labels,preds_constant_bus,label_names)
bus_conmat

print("Constant Opel Matrices\n")
opel_conmat = conmat(test_labels,preds_constant_opel,label_names)
opel_conmat

print("Constant Saab Matrices\n")
saab_conmat = conmat(test_labels,preds_constant_saab,label_names)
saab_conmat

print("Constant Van Matrices\n")
van_conmat = conmat(test_labels,preds_constant_van,label_names)
van_conmat

print("Most Frequent Matrices\n")
most_frequent_conmat = conmat(test_labels,preds_most_frequent,label_names)
most_frequent_conmat

"""### b) kNN

#### kNN Metrics
"""

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier()
knn.fit(train,train_labels)

preds = knn.predict(test)

knn_metrics = mets(test_labels,preds,"kNN")

"""#### kNN Confusion Matrix"""

label_names = np.array(['bus','opel','saab','van'])

print("kNN Matrices\n")
knn_conmat = conmat(test_labels,preds,label_names)
knn_conmat

"""## *** Γ2. Bar Plot ***"""

from matplotlib import pyplot as plt

x_axis = ['F1 Micro','F1 Macro']

ind = np.arange(len(x_axis))

plt.xticks(ind,x_axis)

plt.title("Classifier Metrics")
plt.bar(ind-0.48,knn_metrics,width=0.12,label="KNN") 
plt.bar(ind-0.36,dummy_metrics_default,width=0.12,label="Default")
plt.bar(ind-0.24,dummy_metrics_uniform,width=0.12,label="Uniform") 
plt.bar(ind-0.12,dummy_metrics_bus,width=0.12,label="Bus Const") 
plt.bar(ind,dummy_metrics_opel,width=0.12,label="Opel Const")
plt.bar(ind+0.12,dummy_metrics_saab,width=0.12,label="Saab Const") 
plt.bar(ind+0.24,dummy_metrics_van,width=0.12,label="Van Const")
plt.bar(ind+0.36,dummy_metrics_most_frequent,width=0.12,label="Most Frequent")
plt.legend()

"""## *** Γ3. Σχολιασμός των αποτελεσμάτων ***

Αρχικά παρατηρούμε απο το bar plot πως ο ΚΝΝ δινει τα καλύτερα f1_micro και f1_macro και μάλιστα με τεράστια διαφορά. Συγκεντρωτικά κοιτώντας τα confusion matrices αλλα και το bar plot, μπορούσαμε να υποθέσουμε από την αρχή κιόλας ότι τα ποσοστά των constant dummies και του most_frequent θα ήταν πάρα πολύ χαμηλά αφου το δείγμα μας είναι εξισορροπημένο, οπότε και η υπόθεση ότι κάποια κλαση ήταν κυρίαρχη δε μας έδωσε επιθυμητά αποτελέσματα, αλλά αναμενόμενα. Παρόλο που τα f1_micro, f1_macro ήταν χαμηλά, παρατηρούμε πως και το precision είναι πολύ χαμηλό σε όλα τα constant. Αυτο πρακτικά σημαίνει πως ακόμα και με την υπόθεση ότι υπήρχε κυρίαρχη κλάση, ο dummy classifier "πέτυχε" πολύ λίγα. 

Τελικά λοιπόν η χρήση του ΚΝΝ υπερτερεί αδιαμφισβήτητα στη βελτιστοποίηση της classification.

***
***
# Δ. Βελτιστοποίηση Ταξινομητών
***
***

## Δ1. Βελτιστοποίηση ταξινομητή kNN

### Επιλογή Variance Threshhold

Κληθήκαμε να επιλέξουμε τιμές για το variance threshhold. Αφού υπολογίσαμε το μέγιστο variance να είναι ίσο με περίπου 35000 αποφασίσαμε να δημιουργήσουμε τον πίνακα [0,10000,20000,30000]. Έπειτα από το τρέξιμο του pipe παρατηρήσαμε πως τα βέλτιστα αποτελέσματα ήταν για την τιμή 0 οπότε και αρχίσαμε να μετατοπίζουμε τις τιμές του πίνακα πίνακα σταδιακά προς αυτήν (progressive grid search) μέχρι που φτάσαμε στον τελικό [0,0.001,0.0002,0.0003]. Οπότε σταματήσαμε εκεί αφού πάλι το αποτέλεσμα έβγαινε 0. 

Όταν το δείγμα μας έγινε scaled ξαναυπολογίσαμε το μέγιστο variance και αυτό έβγαινε περίπου 0.06. Ξεκινώντας λοιπόν πάλι με έναν πίνακα [0,0.02,0.004,0.005] καταλήγαμε σε βέλτιστη τιμή το 0. Μειώνοντας 1 τάξη μεγέθους στον πίνακα καταλήξαμε στον τελικό [0,0.0001,0.0002,0.0003,0.0004,0.0005]  κατά τον οποίον τα βέλτιστα αποτελέσματα ίσχυαν είτε για την τιμή 0 είτε για κάποια ενδιάμεση τιμή. Δοκιμάσαμε να τον μειώσουμε κι άλλο άλλα μετά έδιναν όλα 0
"""

# Ευρεση της variance 
train_variance = train.var(axis=0)
print(np.max(train_variance))

# Ευρεση της νέας variance 
from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()
train_minmax = min_max_scaler.fit_transform(train)

train_variance = train_minmax.var(axis=0)
print(np.max(train_variance))

"""### Δομή κώδικα

Μέσα σε 1 for δημιουργούμε μια πεντάδα αριθμών χαρακτηριστική για τον αριθμό του Κ, του Threshhold(-1 αν δεν υπάρχει), του αριθμού των components του PCA(-1 αν δεν υπάρχει) και 1 αν το συγκεκριμένο pipe έχει minmax scaler η -1 αν όχι.

Έτσι διαβάζοντας αυτή την πεντάδα αριθμών μπορούμε να αποφανθούμε για τα βέλτιστα στάδια pipeline που αντιστοιχούν στην βέλτιστη τιμή των f1_micro,f1_macro του train

Ορίζουμε :
- Pipe 1 : kNN
- Pipe 2 : kNN + PCA
- Pipe 3 : kNN + Scaler
- Pipe 4 : kNN + Scaler + PCA
- Pipe 5 : kNN + Threshhold
- Pipe 6 : kNN + Threshhold + PCA
- Pipe 7 : kNN + Scaler + Threshhold
- Pipe 8 : kNN + Scaler + Threshhold + PCA

**Δε θα χρησιμοποιήσουμε καθόλου ROS αφού το δείγμα μας είναι εξισορροπημένο**
"""

from sklearn.model_selection import cross_val_score
import time
from sklearn.feature_selection import VarianceThreshold
from sklearn import preprocessing
from imblearn.over_sampling import RandomOverSampler
from sklearn.decomposition import PCA

mics = []
macs = []

# Εδώ δημιουργούμε μια λίστα result στην οποία κρατάμε τις τιμές των υπερπαραμέτρων σε κάθε εκτέλεση
# Μπορούμε έτσι μετά να βρούμε το index της max τιμής μιας μετρικής και δίνοντάς το στη λίστα να πάρουμε τις βέλτιστες υπερπαραμέτρους.
neighbors = [1,3,5,7,9,11,13]
v_threshhold = [0,0.001,0.002,0.003]
result = []
pipe = range (1,9)

start_time = time.time()

for p in pipe:
  for k in neighbors:
      knn = KNeighborsClassifier(n_neighbors=k)
      # kNN
      if p == 1:
        micro_scores = cross_val_score(knn, train, train_labels, cv=10, scoring='f1_micro')
        macro_scores = cross_val_score(knn, train, train_labels, cv=10, scoring='f1_macro')
        mics.append(micro_scores.mean())
        macs.append(macro_scores.mean())
        result.append([k,-1,-1,1,-1])
      elif p == 2:
        # kNN + PCA
        for n in range(1,train.shape[1]+1):
            pca = PCA(n_components=n)
            trainPCA = pca.fit_transform(train)
            micro_scores = cross_val_score(knn, trainPCA, train_labels, cv=10, scoring='f1_micro')
            macro_scores = cross_val_score(knn, trainPCA, train_labels, cv=10, scoring='f1_macro')
            mics.append(micro_scores.mean())
            macs.append(macro_scores.mean())
            result.append([k,-1,n,2,-1])
      else:
        min_max_scaler = preprocessing.MinMaxScaler()
        train_minmax = min_max_scaler.fit_transform(train)
        
        # kNN + Scaler
        if p == 3:
          micro_scores = cross_val_score(knn, train_minmax, train_labels, cv=10, scoring='f1_micro')
          macro_scores = cross_val_score(knn, train_minmax, train_labels, cv=10, scoring='f1_macro')
          mics.append(micro_scores.mean())
          macs.append(macro_scores.mean())
          result.append([k,-1,-1,3,1])
              
        # kNN + Scaler + PCA
        elif p == 4:
          for n in range(1,train_minmax.shape[1]+1):
              pca = PCA(n_components=n)
              trainPCA = pca.fit_transform(train_minmax)
              micro_scores = cross_val_score(knn, trainPCA, train_labels, cv=10, scoring='f1_micro')
              macro_scores = cross_val_score(knn, trainPCA, train_labels, cv=10, scoring='f1_macro')
              mics.append(micro_scores.mean())
              macs.append(macro_scores.mean())
              result.append([k,-1,n,4,1])
        else:
          for v in v_threshhold:
            selector = VarianceThreshold(v)
            if p > 6:
              train_reduced = selector.fit_transform(train_minmax)
              s = 1
            else:  
              train_reduced = selector.fit_transform(train)
              s = -1

            # Εδώ έχουμε την περίπτωση που έχω είτε kNN + scaler + threshhold(p=7,p=8) είτε kNN + threshhold(p=5,p=6)
            micro_scores = cross_val_score(knn, train_reduced, train_labels, cv=10, scoring='f1_micro')
            macro_scores = cross_val_score(knn, train_reduced, train_labels, cv=10, scoring='f1_macro')
            mics.append(micro_scores.mean())
            macs.append(macro_scores.mean())
            result.append([k,v,-1,p,s])
            # Εδώ έχουμε την περίτωση που έχω είτε  kΝΝ + scaler + threshhold + PCA είτε kΝΝ + threshhold + PCA(p=6,p=8)
            # Ο PCA θέλουμε να τρέξει μόνο για τα συγκεκριμένα pipes
            if p == 6 or p == 8:
              for n in range(1,train_reduced.shape[1]+1):
                pca = PCA(n_components=n)
                trainPCA = pca.fit_transform(train_reduced)
                micro_scores = cross_val_score(knn, trainPCA, train_labels, cv=10, scoring='f1_micro')
                macro_scores = cross_val_score(knn, trainPCA, train_labels, cv=10, scoring='f1_macro')
                mics.append(micro_scores.mean())
                macs.append(macro_scores.mean())
                result.append([k,v,n,p,s])

cv_time = time.time() - start_time

"""### Εύρεση βέλτιστου Pipeline"""

micro_place = mics.index(max(mics))
macro_place = macs.index(max(macs))
mic = result[micro_place]
mac = result[macro_place]

print('Optimum Pipeline for f1-micro is PIPE',mic[3], ', for k_neighbours =',mic[0],'v_threshold =',mic[1],'PCA',mic[2],'and Minmax =',mic[4])
print('Optimum Pipeline for f1-macro is PIPE',mac[3], ', for k_neighbours =',mac[0],'v_threshold =',mac[1],'PCA',mac[2],'and Minmax =',mac[4])

"""** Τώρα, έχοντας βρεί το βέλτιστο pipeline θα πάμε να υπολογίσουμε τα f1_micro,f1_macro για το test  **"""

# Best Micro
start_time = time.time()
knn = KNeighborsClassifier(n_neighbors=mic[0])

min_max_scaler = preprocessing.MinMaxScaler()
train_minmax = min_max_scaler.fit_transform(train)
test_minmax = min_max_scaler.transform(test)

knn.fit(train_minmax,train_labels)
preds_micro = knn.predict(test_minmax)
fp1_time = time.time() - start_time
f1_micro = f1_score(test_labels,preds_micro,average='micro')
print("** Pipe 3 AVG Micro**")
print("f1 micro avg = " ,f1_micro, "\n")


# Best macro
start_time = time.time()
knn = KNeighborsClassifier(n_neighbors=mac[0])

min_max_scaler = preprocessing.MinMaxScaler()
train_minmax = min_max_scaler.fit_transform(train)
test_minmax = min_max_scaler.transform(test)

pca = PCA(n_components=mac[2])
trainPCA = pca.fit_transform(train_minmax)
testPCA = pca.transform(test_minmax)

knn.fit(trainPCA,train_labels)
preds_macro = knn.predict(testPCA)
fp2_time = time.time() - start_time
f1_macro = f1_score(test_labels,preds_macro,average='macro')
print("** Pipe 4 AVG Macro**")
print("f1 macro avg = " ,f1_macro, "\n")

"""### Εκτύπωση Confusion Matrix για τo βέλτιστο Pipeline

Το καλύτερο f1_micro μας βγήκε για το Pipe 3
"""

df_micro = conmat(test_labels,preds_micro,label_names)
df_micro

"""Το καλύτερο f1_macro μας βγήκε για το Pipe 4"""

df_macro = conmat(test_labels,preds_macro,label_names)
df_macro

"""## Δ2. Χρόνοι εκτέλεσης"""

print('Cross Validation time for optimum Pipeline = ',cv_time)
print('Fit - Predict time for optimum Pipeline for micro= ',fp1_time)
print('Fit - Predict time for optimum Pipeline for macro= ',fp2_time)

"""## Δ3. Bar Plot"""

from matplotlib import pyplot as plt

x_axis = ['F1 Micro','F1 Macro']
ind = np.arange(len(x_axis))

plt.xticks(ind,x_axis)

plt.title("Classifier Metrics")

plt.bar(ind,[knn_metrics[0],knn_metrics[1]],width=0.10,label="κΝΝ")
plt.bar(ind+0.12,[f1_micro,f1_macro],width=0.10,label="Pipeline") 

plt.legend()

"""## Δ4. Μεταβολή Επίδοσης kNN"""

dscore = np.array([[knn_metrics[0] ,knn_metrics[1]],
                   [f1_micro,f1_macro],
                   [(f1_micro - knn_metrics[0])/knn_metrics[0]*100,(f1_macro - knn_metrics[1])/knn_metrics[1]*100]])


cols = ['kNN','Pipeline', '% Μεταβολή']

df = pd.DataFrame(dscore.T,columns = cols)
df['F1'] = ['f1_micro','f1_macro']
df.set_index('F1',inplace=True)
df

"""## Δ5. Σχολιασμός των αποτελεσμάτων

Παρατηρούμε βελτίωση του ταξινομητή σε όλα τα pipelines αλλά αυτά που ξεχωρίζουν είναι αυτά στα οποία χρησιμοποιήθηκε ο minmax scaler. Εξ αυτών ξεχωρίζουν τα pipes κΝΝ + scaler και kNN + Scaler + PCA. Στο cross validation μας αποφασίσαμε να εξαντλησουμε σχεδόν όλουςτους πιθανούς συνδυασμούς γι'αυτό και το cv_time μας παίρνει λίγο παραπάνω. Κρίνοντας από το αποτέλεσμα θα μπορούσαμε να το περιορίσουμε πάρα πολύ, αλλά προτιμούμε να δείξουμε τη διαδικασία που το υλοποιήσαμε. Δε χρησιμοποιήσαμε ROS αφου το δείγμα μας ήταν εξισορροπημένο, οπότε και το θεωρήσαμε περιττό. Τέλος παρατηρούμε, όπως υποδεικνύει και ο τελευταίος πίνακας που τυπώσαμε, βελτίωση στο f1_micro κατά 7,55% με χρήση του Pipeline : kNN + scaler, και βελτίωση του f1_macro κατά 11,56% με χρήση του Pipeline : kNN + scaler + PCA
"""