env = Environment()

from tivobuddy import TivoBuddy
from tivobuddydb import Show, TivoBuddyDB
from findtivo import TivoHunter
import pickle

env.CacheDir("./scons_cache_dir")

def get_tivos_on_network(target,source,env):
	a = TivoHunter(maxDuration=30)
	tivodict = a.run_scan()
	for k,v in tivodict.items():
		output = open(k + ".tivo","w")
		output.write(v + "\n")
		output.close()
	return None
bld = Builder(action=get_tivos_on_network,suffix='.tivo',src_suffix='.cfg')
env["BUILDERS"] = {'GetTivo' : bld}
for tivo in Glob("config/tivos/*"):
	env.GetTivo(tivo)
#env.GetTivos(['Cogsworth.tivo','Gaston.tivo','Lumiere.tivo'],['config.cfg'])
tivos = Glob("*.tivo")


