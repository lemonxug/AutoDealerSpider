import pandas as pd
import sys


print('读取csv格式文件：'+ sys.argv[1])
df = pd.read_csv(sys.argv[1])
print('输出为xlsx格式文件：'+ sys.argv[1].split('.')[0]+'.xlsx')
df.to_excel( sys.argv[1].split('.')[0]+'.xlsx', index=None)
print('转换完成！')