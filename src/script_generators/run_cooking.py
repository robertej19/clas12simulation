def run_cooking(scard):
  strn = """ls -l
  set notsouseful_start = `date`
  notsouseful-util -i gemc.hipo -o out_gemc.hipo -c 2
  echo after cooking"""
  return strn
