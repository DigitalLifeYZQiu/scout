import string
import math
import nltk
import re
# nltk.download('punkt')


class getStaticFeature:
    def information_entropy(self, data):
        # print(data)
        if not data:
            return 0
        entropy = 0
        data = data.replace(' ', '')
        for x in range(256):
            p_x = float(data.count(chr(x))) / len(data)
            if p_x > 0:
                entropy += (-p_x * math.log(p_x, 2))
        return entropy

    def coincidence_index(self, data):
        if not data:
            return 0
        char_count = 0
        total_char_count = 0
        # ����ÿһ���ַ����ֵĴ���
        for x in range(256):
            char = chr(x)
            now_char_count = data.count(char)
            char_count += (now_char_count * (now_char_count - 1))
            total_char_count += now_char_count
        # �����غ�ָ���Ĺ�ʽ����
        ic = float(char_count) / (total_char_count * (total_char_count - 1))
        return ic

    def evil_functions(self, data):
        include1 = ['assert', 'eval', 'python_eval', 'shell', 'array_map', 'call_user_func', 'system', 'preg_replace',
                    'passthru', 'shell_exec', 'exec', 'proc_open', 'popen', 'curl_exec', 'curl_multi_exec',
                    'parse_ini_file', 'show_source']
        include2 = ['file_get_contents', 'is_file', 'fopen', 'fclose', 'fwrite', 'wget', 'lynx', 'curl',
                    'posix_getpwuid',
                    'posix_getgrgid', 'fileowner', 'filegroup']
        include3 = ['mysql_connect', 'mysql_query', 'mysql_num_fields', 'mysql_close', 'mysql_fetch_array',
                    'mysql_fetch_assoc', 'mysql_num_rows', 'mysql_result', 'mysql_affected_rows', 'mysql_select_db',
                    'mssql_connect', 'mssql_query', 'mssql_num_fields', 'mssql_field_name', 'mssql_fetch_array',
                    'mysql_close']
        include4 = ['gzdeflat', 'gzcompress', 'gzuncompress', 'gzdecode', 'str_rot13', 'gzencode', 'base64_decode',
                    'base64_encode']
        num1, num2, num3, num4 = 0, 0, 0, 0
        content = nltk.word_tokenize(data)
        # print(content)
        for s in content:
            if len(s) < 2:
                continue
            else:
                if s in include1:
                    num1 += 1
                elif s in include2:
                    num2 += 1
                elif s in include3:
                    num3 += 1
                elif s in include4:
                    num4 += 1
        # print(num1,num2,num3,num4)
        return num1, num2, num3, num4