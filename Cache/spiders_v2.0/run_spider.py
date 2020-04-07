from BuickSpider import BuickSpider
from BydSpider import BydSpider
from ChevroletSpider import ChevroletSpider
from DfcitroenSpider import DfcitroenSpider
from DsSpider import DsSpider
from DykmcSpider import DykmcSpider
from FawvmSpider import FawvmSpider
from FordSpider import FordSpider
from FtmsSpider import FtmsSpider
from GactoyotaSpider import GactoyotaSpider
from GeelySpider import GeelySpider
from GhacSpider import GhacSpider
from GwmSpider import GwmSpider
from HyundaiSpider import HyundaiSpider
from NissanSpider import NissanSpider
from SkodaSpider import SkodaSpider
from SvmSpider import SvmSpider


officialspiders = [
                    BuickSpider,
                    # BydSpider, NG
                    # ChevroletSpider, NG
                    # DfcitroenSpider, NG
                    DsSpider,
                    DykmcSpider,
                    FawvmSpider,
                    # FordSpider, NG
                    FtmsSpider,
                    GactoyotaSpider,
                    GeelySpider,
                    # GhacSpider, NG
                    # HyundaiSpider, NG
                    # NissanSpider, NG
                    SkodaSpider,
                    # SvmSpider, NG
                    # GwmSpider, # 未完成
                   ]


if __name__ == '__main__':
    for spider in officialspiders:
        s = spider()
        s.run()

# dyk = DykmcSpider()
# dyk.run()

# import os
# officialspiders = []
# for f in os.listdir('./'):
#     if '.py' in f:
#         print('from '+f.split('.')[0]+' import '+ f.split('.')[0])
#         officialspiders.append(f.split('.')[0])
# print(officialspiders)

