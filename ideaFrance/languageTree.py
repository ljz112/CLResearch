######### IN USE FOR PROJECT


#### my language categorization method but in a python dict/list format

# afroasiatic
afroasiatic = {}
afroasiatic['language'] = 'afroasiatic'

ar = {}
ar['language'] = 'ar'

aa = {}
aa['language'] = 'aa'
aa['children'] = []
ma = {}
ma['language'] = 'ma'
ma['children'] = []
mga = {}
mga['language'] = 'mga'
mga['children'] = []
ear = {}
ear['language'] = 'ear'
ear['children'] = []

ar['children'] = [aa, ma, mga, ear]

brb = {}
brb['language'] = 'brb'
brb['children'] = []
hb = {}
hb['language'] = 'hb'
hb['children'] = []

afroasiatic['children'] = [ar, brb, hb]

# native american
native_american = {}
native_american['language'] = 'native_american'

eskimo_aleut = {}
eskimo_aleut['language'] = 'eskimo_aleut'

gld = {}
gld['language'] = 'gld'
gld['children'] = []
inuk = {}
inuk['language'] = 'int'
inuk['children'] = []

eskimo_aleut['children'] = [gld, inuk]

tno = {}
tno['language'] = 'tno'
tno['children'] = []
qch = {}
qch['language'] = 'qch'
qch['children'] = []

native_american['children'] = [eskimo_aleut, tno, qch]

msh = {}
msh['language'] = 'msh'
msh['children'] = []

# creoles
creoles = {}
creoles['language'] = 'creoles'

ant = {}
ant['language'] = 'ant'
ant['children'] = []
htc = {}
htc['language'] = 'htc'
htc['children'] = []
jmc = {}
jmc['language'] = 'jmc'
jmc['children'] = []
ktb = {}
ktb['language'] = 'ktb'
ktb['children'] = []
snt = {}
snt['language'] = 'snt'
snt['children'] = []

creoles['children'] = [ant, htc, jmc, ktb, snt]

# tamil (only dravidan language)
tml = {}
tml['language'] = 'tml'
tml['children'] = []

# thai (only kra-dai language)
thi = {}
thi['language'] = 'thi'
thi['children'] = []

# luo (only nilo-saharan language)
lo = {}
lo['language'] = 'lo'
lo['children'] = []

# indo-european
indo_european = {}
indo_european['language'] = 'indo_european'

romance = {}
romance['language'] = 'romance'

fr = {}
fr['language'] = 'fr'

ofs = {}
ofs['language'] = 'ofs'
ofs['children'] = []

fr['children'] = [ofs]

crs = {}
crs['language'] = 'crs'
crs['children'] = []
es = {}
es['language'] = 'es'

mxs = {}
mxs['language'] = 'mxs'
mxs['children'] = []
esa = {}
esa['language'] = 'esa'
esa['children'] = []
esq = {}
esq['language'] = 'esq'
esq['children'] = []
est = {}
est['language'] = 'est'
est['children'] = []
ctn = {}
ctn['language'] = 'ctn'
ctn['children'] = []
vcn = {}
vcn['language'] = 'vcn'
vcn['children'] = []

es['children'] = [mxs, esa, esq, est, ctn, vcn]

it = {}
it['language'] = 'it'

vnt = {}
vnt['language'] = 'vnt'
vnt['children'] = []

it['children'] = [vnt]

pt = {}
pt['language'] = 'pt'

pmd = {}
pmd['language'] = 'pmd'
pmd['children'] = []

pt['children'] = [pmd]

romance['children'] = [fr, crs, es, it, pt]

germanic = {}
germanic['language'] = 'germanic'

de = {}
de['language'] = 'de'

ald = {}
ald['language'] = 'ald'
ald['children'] = []

de['children'] = [ald]

yd = {}
yd['language'] = 'yd'
yd['children'] = []

afk = {}
afk['language'] = 'afk'
afk['children'] = []

nl = {}
nl['language'] = 'nl'
nl['children'] = []

en = {}
en['language'] = 'en'

ve = {}
ve['language'] = 've'
ve['children'] = []
eni = {}
eni['language'] = 'eni'
eni['children'] = []
ens = {}
ens['language'] = 'ens'
ens['children'] = []

en['children'] = [ve, eni, ens]

germanic['children'] = [de, yd, afk, nl, en]

slv = {}
slv['language'] = 'slv'

ru = {}
ru['language'] = 'ru'
ru['children'] = []
sc = {}
sc['language'] = 'sc'
sc['children'] = []
pl = {}
pl['language'] = 'pl'
pl['children'] = []

slv['children'] = [ru, sc, pl]

indo_iranian = {}
indo_iranian['language'] = 'indo_iranian'

indo_aryan = {}
indo_aryan['language'] = 'indo_aryan'

rm = {}
rm['language'] = 'rm'
rm['children'] = []
hs = {}
hs['language'] = 'hs'

hin = {}
hin['language'] = 'hin'
hin['children'] = []

hs['children'] = [hin]

indo_aryan['children'] = [rm, hs]

pr = {}
pr['language'] = 'pr'
pr['children'] = []

indo_iranian['children'] = [indo_aryan, pr]

gr = {}
gr['language'] = 'gr'
gr['children'] = []

indo_european['children'] = [romance, germanic, slv, indo_iranian, gr]

# east asian
east_asian = {}
east_asian['language'] = 'east_asian'

sino_tibetan = {}
sino_tibetan['language'] = 'sino_tibetan'

tbt = {}
tbt['language'] = 'tbt'
tbt['children'] = []
chinese = {}
chinese['language'] = 'chinese'

cnc = {}
cnc['language'] = 'cnc'
cnc['children'] = []
cnm = {}
cnm['language'] = 'cnm'
cnm['children'] = []
cnh = {}
cnh['language'] = 'cnh'
cnh['children'] = []

chinese['children'] = [cnc, cnm, cnh]

sino_tibetan['children'] = [tbt, chinese]

jp = {}
jp['language'] = 'jp'
jp['children'] = []
kr = {}
kr['language'] = 'kr'
kr['children'] = []

east_asian['children'] = [sino_tibetan, jp, kr]

# niger-congo
niger_congo = {}
niger_congo['language'] = 'niger_congo'

bantu = {}
bantu['language'] = 'bantu'

swh = {}
swh['language'] = 'swh'
swh['children'] = []
zl = {}
zl['language'] = 'zl'
zl['children'] = []
lga = {}
lga['language'] = 'lga'
lga['children'] = []

bantu['children'] = [swh, zl, lga]

bb = {}
bb['language'] = 'bb'
bb['children'] = []
wlf = {}
wlf['language'] = 'wlf'
wlf['children'] = []

niger_congo['children'] = [bantu, bb, wlf]

dha = {}
dha['language'] = 'dha'
dha['children'] = []
tr = {}
tr['language'] = 'tr'
tr['children'] = []

uralic = {}
uralic['language'] = 'uralic'

fn = {}
fn['language'] = 'fn'
fn['children'] = []
mg = {}
mg['language'] = 'mg'
mg['children'] = []

uralic['children'] = [fn, mg]

bsq = {}
bsq['language'] = 'bsq'
bsq['children'] = []

LANGUAGE_TREE = [afroasiatic, native_american, msh, creoles, tml, thi, lo, indo_european, east_asian, niger_congo, dha, tr, uralic, bsq]