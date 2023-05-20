import os
import subprocess
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import re

class getDynamicFeature:
    def get_opcodes(self,fullpath):
        (filename, extension) = os.path.splitext(fullpath)
        # ע��һ������.php������
        if extension == ".php":
            try:
                output = subprocess.check_output(["php", "-dvld.active=1", "-dvld.execute=0", fullpath],
                                                 stderr=subprocess.STDOUT).decode("utf-8")  # ��php���opcode
                # print(output)
                getopcodes = re.findall(r"\s(\b[A-Z_]+\b)\s", output)  # ��д���ʶ��õ�
                # print(getopcodes)
                # �о����ܽ���ȥ�أ�����Ҫʹ��textrank�㷨��ͼ���������Ӱ�졣
                # getopcodes=np.unique(getopcodes)
                # getopcodes=getopcodes.tolist()
                # ͬʱ������textrank�㷨�����һ��Ϊ�ַ���������������Ҫ����һ��
                getopcodes=" ".join(getopcodes).replace("E O E ",'')
                # �����ȡ�Ķ���δ��ת��������ԭʼ�Ĵ�д��opcodes
                return getopcodes
            except:
                print("get_opcodes error!")

    # �ڽ���textrank�㷨��ȡ����ֵ֮ǰ���������ǿ��Գ�����ȡwebshell��opcodes�ĳ������ֵĹؼ��ʣ�����opcode��ɵ��ı�������textrank�ķִʴ����Ĺؼ���
    def get_textrankopcodes(self,opcodes,textrank_opcodes):
        tr4kw=TextRank4Keyword()
        tr4kw.analyze(text=opcodes,lower=True,window=2)
        for item in tr4kw.get_keywords(num=200,word_min_len=1):
            textrank_opcodes.append(item.word)
        return textrank_opcodes

    def get_textrankvalue(self,opcodes):  # ����һ���б� 92��ֵ
        # ǰ��get_textrankopcodes����ȡ����webshell�д��ڵ�92���ؼ��ʣ���92������
        textrank_opcodes_dict={'add': 0, 'arg': 0, 'args': 0, 'array': 0, 'assert': 0, 'assign': 0, 'bind': 0, 'bool': 0, 'bw': 0, 'call': 0, 'case': 0, 'cast': 0, 'catch': 0, 'check': 0, 'class': 0, 'concat': 0, 'connect': 0, 'constant': 0, 'count': 0, 'cv': 0, 'data': 0, 'db': 0, 'dec': 0, 'declare': 0, 'defined': 0, 'dim': 0, 'div': 0, 'dynamic': 0, 'echo': 0, 'element': 0, 'equal': 0, 'eval': 0, 'exit': 0, 'ext': 0, 'fast': 0, 'fcall': 0, 'fe': 0, 'fetch': 0, 'free': 0, 'func': 0, 'function': 0, 'global': 0, 'identical': 0, 'include': 0, 'init': 0, 'isempty': 0, 'isset': 0, 'jmp': 0, 'jmpnz': 0, 'jmpz': 0, 'lambda': 0, 'list': 0, 'listen': 0, 'long': 0, 'method': 0, 'mod': 0, 'msql': 0, 'mul': 0, 'net': 0, 'nop': 0, 'num': 0, 'obj': 0, 'op': 0, 'post': 0, 'pre': 0, 'prop': 0, 'protocol': 0, 'qm': 0, 'recv': 0, 'ref': 0, 'require': 0, 'reset': 0, 'return': 0, 'rope': 0, 'rw': 0, 'send': 0, 'silence': 0, 'sl': 0, 'smaller': 0, 'socket': 0, 'sr': 0, 'static': 0, 'stmt': 0, 'string': 0, 'strlen': 0, 'switch': 0, 'type': 0, 'unset': 0, 'user': 0, 'val': 0, 'var': 0, 'xor': 0}
        tr4kw=TextRank4Keyword()
        # ������Сдת��������ֵΪ2����������֮��ı�Ĭ��ֵΪ2������2������
        tr4kw.analyze(text=opcodes,lower=True,window=2)
        # ��ȡ����Ҫ��num��ֵ����С����Ϊword_min_len�Ĺؼ���
        for item in tr4kw.get_keywords(num=100,word_min_len=1):
            # print(item.word,item.weight)
            if item.word in textrank_opcodes_dict:
                textrank_opcodes_dict[item.word]=item.weight  # opcode���о͸ĳɶ�Ӧ��Ȩֵ��û�оͻ���0
        # ֻ���ض�Ӧ��ֵ������Ҫdict
        textrank_opcodes_value=[]
        for key,value in textrank_opcodes_dict.items():
            textrank_opcodes_value.append(value)
        return textrank_opcodes_value