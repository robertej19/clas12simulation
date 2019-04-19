def run_gemc(scard):
  strn = """ls -l
  set gemc_start = `date`
  gemc -USE_GUI=0 -N={0} -INPUT_GEN_FILE="lund, {1}"{2} {3}
  echo after gemc""".format(scard.nevents,scard.gcard,scard.gevent,scard.other)
  return strn
