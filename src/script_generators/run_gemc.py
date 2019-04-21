def run_gemc(scard):
  strn = """\n\nls -l
set gemc_start = `date`
gemc -USE_GUI=0 -N={0} -INPUT_GEN_FILE="lund, {1}" {2} {3}
echo after gemc\n""".format(scard.data['nevents'],scard.data['genOutput'],scard.data['luminosity'],"scard.data['gcards']")
  return strn
