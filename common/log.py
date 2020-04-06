import logging


class log():

    def ll(self,logs_path):
        #创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        #创建一个handler，用于写入日志文件
        #logs_path = "./logs/api_log.txt" # 指定文件输出路径，注意logs是个文件夹，一定要加上/，不然会导致输出路径错误，把logs变成文件名的一部分了
        fh = logging.FileHandler(logs_path,mode='a',encoding = 'utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
        fh.setLevel(logging.DEBUG)

        #创建一个handler，用于将日志输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - '
                                      '%(levelname)s - '
                                      '%(filename)s[line:%(lineno)d] - '
                                      '%(funcName)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger


