import sys

# 保留字
_key = ('program', 'type', 'integer', 'char', 'var', 'begin', 'end', 'read', 'write', 'while', 'if',
        'procedure', 'array', 'of', 'record', 'then', 'else', 'fi', 'do', 'endwh', 'return'
        )
# 分界符
_siginal = {'+': 'PLUS', '-': 'MINUS', '*': 'TIMES', '/': 'OVER', '(': 'LPAREN', ')': 'RPAREN',
            ';': 'SEMI', '[': 'LMIDPAREN', ']': 'RMIDPAREN', '=': 'EQ', '<': 'LT', 'EOF': 'ENDFILE',
            '..':'UNDERANGE'}
_token = ''
_tabNum = 0

_tokenNum = 0

# 函数声明



def printTab():
	i = 0
	while i < _tabNum:
		print('   ', end = ' ')
		i += 1

def parseError():
	print("{0} : error".format(get_token[_tokenNum][0]))
	sys.exit(1)

def get_content():
	global _token
	token = open(r'E:\token.txt', 'r')
	for line in token:
		_token = "%s%s" %(_token, line.lstrip())
	token_list = _token.split('\n')
	_token = []
	for c in token_list:
		temp = c.split(' ')
		_token.append(temp)
	#print(_token)
	return _token
	
#def get_token(n):
#	global _token, line_num, lexical_info, semantic_info
#	token = open(r'E:\token.txt', 'r')
#	for line in token:
#		#line1 = tuple(line)
#		_token = "%s%s" %(_token, line.lstrip())
#	token_list = _token.split('\n')
#	_token = []
#	for c in token_list: 
#		temp = c.split(' ')
#		_token.append(temp)
#	line_num = _token[n][0]
#	lexical_info = _token[n][1]
#	semantic_info = _token[n][2]
#	#print(_token)
#	return (line_num, lexical_info, semantic_info)

def match(token):
	global _tokenNum,currToken
	#currToken = get_token(_tokenNum)[1]
	if currToken == token:
		printTab()
		print("%s" %get_token[_tokenNum][2])
		#if token == 'ID' or token == 'INTC':
		#	print("%s" %get_token(_tabNum)[2])
		#elif token.lower() in _key:
		#	print("%s" %token.lower())
		#else:
		#	for key1 in _siginal: 
		#		if token == _siginal[key1]: 
		#			print("%s" %key1)
		_tokenNum += 1
		currToken = get_token[_tokenNum][1]
	else:
		parseError()


def Program():
	global _tabNum, _tokenNum
	printTab()
	print("Program")
	_tabNum += 1
	#currToken = get_token(_tokenNum)[1]
	#print("currToken =",currToken)
	if currToken == 'PROGRAM':
		ProgramHead()
		DeclarePart()
		ProgramBody()
		#print("find it") 
	else:
		parseError()
	_tabNum -= 1 

def ProgramHead():
	global _tabNum, currToken
	printTab()
	print("ProgramHead")
	_tabNum += 1
	#currToken = get_token(_tokenNum)[1]
	if currToken == 'PROGRAM': 
		match('PROGRAM')
		ProgramName()
	else:
		parseError() 
	_tabNum -= 1

def ProgramName():
	global _tabNum, currToken
	printTab() 
	print("ProgramName")
	_tabNum += 1
	if currToken == 'ID':
		match('ID')
	else:
		parseError()
	_tabNum -= 1

def DeclarePart(): 
	global _tabNum, currToken
	printTab()
	print("DeclarePart")
	_tabNum += 1
	if currToken in ['TYPE', 'VAR', 'PROCEDURE', 'BEGIN']: 
		TypeDecpart()
		VarDecpart()
		ProcDecpart()
	else:
		parseError()
	_tabNum -= 1

def TypeDecpart():
	global _tabNum, currToken
	printTab() 
	print("TypeDecpart")
	_tabNum += 1
	if currToken in ['VAR', 'PROCEDURE', 'BEGIN']: 
		pass
	elif currToken == 'TYPE':
		TypeDec()
	else:
		parseError()
	_tabNum -= 1

def TypeDec():
	global _tabNum, currToken
	printTab()
	print("TypeDec")
	_tabNum += 1
	if currToken == 'TYPE':
		match('TYPE')
		TypeDecList() 
	else:
		parseError()
	_tabNum -= 1

def TypeDecList():
	global _tabNum, currToken
	printTab()
	print("TypeDecList")
	_tabNum += 1
	if currToken == 'ID':
		TypeId()
		match('EQ')
		TypeDef()
		match('SEMI')
		TypeDecMore() 
	else:
		parseError()
	_tabNum -= 1

def TypeDecMore():
	global _tabNum, currToken
	printTab()
	print("TypeDecMore")
	_tabNum += 1
	if currToken in ['VAR', 'PROCEDURE', 'BEGIN']:
		pass
	elif currToken == 'ID':
		TypeDecList()
	else:
		parseError()
	_tabNum -= 1

def TypeId():
	global _tabNum, currToken
	printTab()
	print("TypeId")
	_tabNum += 1
	if currToken == 'ID':
		match('ID')
	else:
		parseError()
	_tabNum -= 1

def TypeDef():
	global _tabNum, currToken
	printTab()
	print("TypeDef")
	_tabNum += 1
	if currToken == 'INTEGER' or currToken == 'CHAR':
		BaseType();
	elif currToken == 'ARRAY' or currToken == 'RECORD':
		StructureType()
	elif currToken == 'ID':
		match('ID')
	else:
		parseError()
	_tabNum -= 1

def BaseType():
	global _tabNum, currToken
	printTab()
	print("BastType")
	_tabNum += 1
	if currToken == 'INTEGER':
		match('INTEGER')
	elif currToken == 'CHAR':
		match('CHAR')
	else:
		parseError()
	_tabNum -= 1

def StrucetureType():
	global _tabNum, currToken
	printTab()
	print("StrucetureType")
	_tabNum += 1
	if currToken == 'ARRAY':
		ArrayType()
	elif currToken == 'RECORD':
		RecType()
	else:
		parseError()
	_tabNum -= 1

def ArrayType():
	global _tabNum, currToken
	printTab()
	print("ArrayType")
	_tabNum += 1
	if currToken == 'ARRAY':
		match('ARRAY')
		match('LMIDPAREN')
		Low()
		match('UNDERANGE')
		Top()
		match('RMIDPAREN')
		match('OF')
		BaseType()
	else:
		parseError()
	_tabNum -= 1

def Low():
	global _tabNum, currToken
	printTab()
	print("")
	_tabNum += 1
	if currToken == 'INTC':
		match('INTC')
	else:
		parseError()
	_tabNum -= 1

def Top():
	global _tabNum, currToken
	printTab()
	print("")
	_tabNum += 1
	if currToken == 'INTC':
		match('INTC')
	else:
		parseError()
	_tabNum -= 1

def RecType():
	global _tabNum, currToken
	printTab()
	print("RecType")
	_tabNum += 1
	if currToken == 'RECORD':
		match('RECORD')
		FieldDecList()
		match('END')
	else:
		parseError()
	_tabNum -= 1

def FieldDecList():
	global _tabNum, currToken
	printTab()
	print("FieldDecList")
	_tabNum += 1
	if currToken == 'INTEGER' or currToken == 'CHAR':
		BaseType()
		IdList()
		match('SEMI')
		FieldDecMore()
	elif currToken == 'ARRAY':
		ArrayType()
		IdList()
		match('SEMI')
		FieldDecMore()
	else:
		parseError()
	_tabNum -= 1

def FieldDecMore():
	global _tabNum, currToken
	printTab()
	print("FieldDecMore")
	_tabNum += 1
	if currToken == 'END':
		pass
	elif currToken in ['INTEGER', 'CHAR', 'ARRAY']:
		FieldDecList()
	else:
		parseError()
	_tabNum -= 1

def IdList():
	global _tabNum, currToken
	printTab()
	print("IdList")
	_tabNum += 1
	if currToken == 'ID':
		match('ID')
		IdMore()
	else:
		parseError()
	_tabNum -= 1

def IdMore():
	global _tabNum, currToken
	printTab()
	print("IdMore")
	_tabNum += 1
	if currToken == 'SEMI':
		pass
	elif currToken == 'COMMA':
		match('COMMA')
		IdList()
	else:
		parseError()
	_tabNum -= 1

def VarDecpart():
	global _tabNum, currToken
	printTab()
	print("VarDecpart")
	_tabNum += 1
	if currToken == 'PROCEDURE' or currToken == 'BEGIN': 
		pass
	elif currToken == 'VAR':
		VarDec()
	else:
		parseError()
	_tabNum -= 1

def VarDec():
	global _tabNum, currToken
	printTab()
	print("VarDec")
	_tabNum += 1
	if currToken == 'VAR':
		match('VAR')
		VarDecList()
	else:
		parseError()
	_tabNum -= 1

def VarDecList():
	global _tabNum, currToken
	printTab()
	print("VarDecList")
	_tabNum += 1
	if currToken in ['INTEGER', 'CHAR', 'ARRAY', 'RECORD', 'ID']:
		TypeDef()
		VarIdList()
		match('SEMI')
		VarDecMore()
	else:
		parseError()
	_tabNum -= 1

def VarDecMore():
	global _tabNum, currToken
	printTab()
	print("VarDecMore")
	_tabNum += 1
	if currToken == 'PROCEDURE' or currToken == 'BEGIN':
		pass
	elif currToken in ['INTEGER', 'CHAR', 'ARRAY', 'RECORD', 'ID']:
		VarDecList()
	else:
		parseError()
	_tabNum -= 1

def VarIdList():
	global _tabNum, currToken
	printTab()
	print("VarIdList")
	_tabNum += 1
	if currToken == 'ID':
		match('ID')
		#print('find it')
		VarIdMore()
	else:
		parseError()
	_tabNum -= 1

def VarIdMore():
	global _tabNum, currToken
	printTab()
	print("VarIdMore")
	_tabNum += 1
	if currToken == 'SEMI':
		pass
	elif currToken == 'COMMA':
		match('COMMA')
		VarIdList()
	else:
		parseError()
	_tabNum -= 1

def ProcDecpart():
	global _tabNum, currToken
	printTab()
	print("ProcDecpart")
	_tabNum += 1
	if currToken == 'BEGIN':
		pass
	elif currToken == 'PROCEDURE':
		ProcDec()
	else:
		parseError()
	_tabNum -= 1

def ProcDec():
	global _tabNum, currToken
	printTab()
	print("ProcDec")
	_tabNum += 1
	if currToken == 'PROCEDURE':
		match('PROCEDURE')
		ProcName()
		match('LPAREN')
		ParamList() 
		match('RPAREN')
		match('SEMI')
		ProcDecPart()
		ProcBody()
		ProcDecMore()
	else:
		parseError()
	_tabNum -= 1

def ProcDecMore():
	global _tabNum, currToken
	printTab()
	print("ProcDecMore")
	_tabNum += 1
	if currToken == 'BEGIN':
		pass
	elif currToken == 'PROCEDURE':
		ProcDec()
	else:
		parseError() 
	_tabNum -= 1

def ProcName():
	global _tabNum, currToken
	printTab()
	print("ProcName")
	_tabNum += 1
	if currToken == 'ID':
		match('ID')
	else:
		parseError()
	_tabNum -= 1

def ParamList():
	global _tabNum, currToken
	printTab()
	print("ParamList")
	_tabNum += 1
	if currToken == 'RPAREN':
		pass
	elif currToken in ['INTEGER', 'CHAR', 'ARRAY', 'RECORD', 'ID', 'VAR']:
		ParamDecList()
	else:
		parseError()
	_tabNum -= 1

def ParamDecList():
	global _tabNum, currToken
	printTab()
	print("ParamDecList")
	_tabNum += 1
	if currToken in ['INTEGER', 'CHAR', 'ARRAY', 'RECORD', 'ID', 'VAR']:
		Param()
		ParamMore()
	else:
		parseError()
	_tabNum -= 1

def ParamMore():
	global _tabNum, currToken
	printTab()
	print("ParamMore")
	_tabNum += 1
	if currToken == 'RPAREN':
		pass
	elif currToken == 'SEMI':
		match('SEMI')
		ParamDecList()
	else:
		parseError()
	_tabNum -= 1

def Param():
	global _tabNum, currToken
	printTab()
	print("Param")
	_tabNum += 1
	if currToken in ['INTEGER', 'CHAR', 'ARRAY', 'RECORD', 'ID']:
		TypeDef()
		FromList()
	else:
		parseError()
	_tabNum -= 1

def FromList():
	global _tabNum, currToken
	printTab()
	print("FromList")
	_tabNum += 1
	if currToken == 'ID':
		match('ID')
		FidMore()
	else:
		parseError()
	_tabNum -= 1

def FidMore():
	global _tabNum, currToken
	printTab()
	print("FidMore")
	_tabNum += 1
	if currToken == 'SEMI' or currToken == 'RPAREN':
		pass
	elif currToken == 'COMMA':
		match('COMMA')
		FromList()
	else:
		parseError()
	_tabNum -= 1

def ProcDecPart():
	global _tabNum, currToken
	printTab()
	print("ProcDecPart")
	_tabNum += 1
	if currToken in ['TYPE', 'VAR', 'PROCEDURE', 'BEGIN']:
		DeclarePart()
	else:
		parseError()
	_tabNum -= 1

def ProcBody():
	global _tabNum, currToken
	printTab()
	print("ProcBody")
	_tabNum += 1
	if currToken == 'BEGIN':
		ProgramBody()
	else:
		parseError()
	_tabNum -= 1

def ProgramBody():
	global _tabNum, currToken
	printTab()
	print("ProgramBody")
	_tabNum += 1
	if currToken == 'BEGIN':
		match('BEGIN')
		StmList()
		match('END')
	else:
		parseError()
	_tabNum -= 1

def StmList():
	global _tabNum, currToken
	printTab()
	print("StmList")
	_tabNum += 1
	if currToken in ['ID', 'IF', 'WHILE', 'RETURN', 'READ', 'WRITE']:
		Stm()
		StmMore()
	else:
		parseError()
	_tabNum -= 1

def StmMore():
	global _tabNum, currToken
	printTab()
	print("StmMore")
	_tabNum += 1
	if currToken in ['ELSE', 'FI', 'END', 'ENDWH']:
		pass
	elif currToken == 'SEMI':
		match('SEMI')
		StmList() 
	else:
		parseError()
	_tabNum -= 1

def Stm():
	global _tabNum, currToken
	printTab()
	print("Stm")
	_tabNum += 1
	if currToken == 'IF':
		ConditionalStm()
	elif currToken == 'WHILE':
		LoopStm()
	elif currToken == 'READ':
		InputStm()
	elif currToken == 'WRITE':
		OutputStm()
	elif currToken == 'RETURN':
		ReturnStm()
	elif currToken == 'ID':
		match('ID')
		AssCall()
	else:
		parseError()
	_tabNum -= 1

def  AssCall():
	global _tabNum, currToken
	printTab()
	print("AssCall")
	_tabNum += 1
	if currToken in ['ASSIGN', 'LMIDPAREN', 'DOT']:
		AssignmentRest()
	elif currToken == 'LPAREN':
		CallStmRest()
	else:
		parseError()
	_tabNum -= 1

def AssignmentRest():
	global _tabNum, currToken
	printTab()
	print("AssignmentRest")
	_tabNum += 1
	if currToken in ['LMIDPAREN', 'DOT', 'ASSIGN']:
		VariMore()
		match('ASSIGN')
		Exp()
	else:
		parseError()
	_tabNum -= 1

def ConditionalStm():
	global _tabNum, currToken
	printTab()
	print("ConditionalStm")
	_tabNum += 1
	if currToken == 'IF':
		match('IF')
		RelExp()
		match('THEN')
		StmList()
		match('ELSE')
		StmList()
		match('FI')
	else:
		parseError()
	_tabNum -= 1

def LoopStm():
	global _tabNum, currToken
	printTab()
	print("LoopStm")
	_tabNum += 1
	if currToken == 'WHILE':
		match('WHILE')
		RelExp()
		match('DO')
		StmList()
		match('ENDWH')
	else:
		parseError()
	_tabNum -= 1

def InputStm():
	global _tabNum, currToken
	printTab()
	print("InputStm")
	_tabNum += 1
	if currToken == 'READ':
		match('READ')
		match('LPAREN')
		Invar()
		match('RPAREN')
	else:
		parseError()
	_tabNum -= 1

def Invar():
	global _tabNum, currToken
	printTab()
	print("Invar")
	_tabNum += 1
	if currToken == 'ID':
		match('ID')
	else:
		parseError()
	_tabNum -= 1

def OutputStm():
	global _tabNum, currToken
	printTab()
	print("OutputStm")
	_tabNum += 1
	if currToken == 'WRITE':
		match('WRITE')
		match('LPAREN')
		Exp()
		match('RPAREN')
	else:
		parseError()
	_tabNum -= 1

def ReturnStm():
	global _tabNum, currToken
	printTab()
	print("ReturnStm")
	_tabNum += 1
	if currToken == 'RETURN':
		match(RETURN)
	else:
		parseError()
	_tabNum -= 1

def CallStmRest():
	global _tabNum, currToken
	printTab()
	print("CallStmRest")
	_tabNum += 1
	if currToken == 'LPAREN':
		match('LPAREN')
		ActParamList()
		match('RPAREN')
	else:
		parseError()
	_tabNum -= 1

def ActParamList():
	global _tabNum, currToken
	printTab()
	print("ActParamList")
	_tabNum += 1
	if currToken == 'RPAREN':
		pass
	elif currToken in ['LPAREN', 'INTC', 'ID']:
		Exp()
		ActParamMore()
	else:
		parseError()
	_tabNum -= 1

def ActParamMore():
	global _tabNum, currToken
	printTab()
	print("ActParamMore")
	_tabNum += 1
	if currToken == 'COMMA':
		match('COMMA')
		ActParamList()
	elif currToken == 'RPAREN':
		pass
	else:
		parseError()
	_tabNum -= 1

def RelExp():
	global _tabNum, currToken
	printTab()
	print("RelExp")
	_tabNum += 1
	if currToken in ['LPAREN', 'INTC', 'ID']:
		Exp()
		OtherRelE()
	else:
		parseError()
	_tabNum -= 1

def OtherRelE():
	global _tabNum, currToken
	printTab()
	print("OtherRelE")
	_tabNum += 1
	if currToken == 'LT' or currToken == 'EQ':
		CmpOp()
		Exp()
	else:
		parseError()
	_tabNum -= 1

def Exp():
	global _tabNum, currToken
	printTab()
	print("Exp")
	_tabNum += 1
	if currToken in ['LPAREN', 'INTC', 'ID']:
		Term()
		OtherTerm()
	else:
		parseError()
	_tabNum -=1

def OtherTerm():
	global _tabNum, currToken
	printTab()
	print("OtherTerm")
	_tabNum += 1
	if currToken in ['LT', 'EQ', 'RMIDPAREN', 'THEN', 'ELSE', 'FI', 'DO', 'ENDWH', 'RPAREN', 'END', 'SEMI', 'COMMA']:
		pass
	elif currToken == 'PLUS' or currToken == 'MINUS':
		AddOp()
		Exp()
	else:
		parseError()
	_tabNum -= 1

def Term():
	global _tabNum, currToken
	printTab()
	print("Term")
	_tabNum += 1
	if currToken in ['LPAREN', 'INTC', 'ID']:
		Factor()
		OtherFactor()
	else:
		parseError()
	_tabNum -= 1

def OtherFactor():
	global _tabNum, currToken
	printTab()
	print("OtherFactor")
	_tabNum += 1
	if currToken in ['PLUS', 'MINUS', 'LT', 'EQ', 'LMIDPAREN', 'THEN', 'ELSE', 'FI', 'DO', 'ENDWH', 'RPAREN', 'END', 'SEMI', 'COMMA', 'RMIDPAREN']:
		pass
	elif currToken == 'TIMES' or currToken == 'OVER':
		MultOp()
		Term()
	else:
		parseError()
	_tabNum -= 1

def Factor():
	global _tabNum, currToken
	printTab()
	print("Factor")
	_tabNum += 1
	if currToken == 'LPAREN':
		match('LPAREN')
		Exp()
		match('RPAREN')
	elif currToken == 'INTC':
		match('INTC')
	elif currToken == 'ID':
		Variable()
	else:
		parseError() 
	_tabNum -= 1

def Variable():
	global _tabNum, currToken
	printTab()
	print("Variable")
	_tabNum += 1
	if currToken == 'ID':
		match('ID')
		VariMore()
	else:
		parseError()
	_tabNum -= 1

def VariMore():
	global _tabNum, currToken
	printTab()
	print("VariMore")
	_tabNum += 1
	if currToken in ['ASSIGN', 'TIMES', 'OVER', 'PLUS', 'MINUS', 'LT', 'EQ', 'THEN', 'ELSE', 'FI', 'DO', 'ENDWH', 'RPAREN', 'END', 'SEMI', 'COMMA', 'RMIDPAREN']:
		pass
	elif currToken == 'LMIDPAREN':
		match('LMIDPAREN')
		Exp()
		match('RMIDPAREN')
	elif currToken == 'DOT':
		match('DOT')
		FieldVar()
	else:
		parseError()
	_tabNum -= 1

def FieldVar():
	global _tabNum, currToken
	printTab()
	print("FieldVar")
	_tabNum += 1
	if currToken == 'ID':
		match('ID')
		FieldVarMore()
	else:
		parseError()
	_tabNum -= 1

def FieldVarMore():
	global _tabNum, currToken
	printTab()
	print("FieldVarMore")
	_tabNum += 1
	if currToken in ['ASSIGN', 'TIMES', 'OVER', 'EQ', 'LT', 'PLUS', 'MINUS', 'RPAREN', 'SEMI', 'COMMA', 'THEN', 'ELSE', 'FI', 'DO', 'ENDWH', 'END']:
		pass
	elif currToken == 'LMIDPAREN':
		match('LMIDPAREN')
		Exp()
		match('RMIDPAREN')
	else:
		parseError()
	_tabNum -= 1

def CmpOp():
	global _tabNum, currToken
	printTab()
	print("CmpOp")
	_tabNum += 1
	if currToken == 'LT':
		match('LT')
	elif currToken == 'EQ':
		match('EQ')
	else:
		parseError()
	_tabNum -= 1

def AddOp():
	global _tabNum, currToken
	printTab()
	print("AddOp")
	_tabNum += 1
	if currToken == 'PLUS':
		match('PLUS')
	elif currToken == 'MINUS':
		match('MINUS')
	else:
		parseError()
	_tabNum -= 1

def MultOp():
	global _tabNum, currToken
	printTab()
	print("MultOp")
	_tabNum += 1
	if currToken == 'TIMES':
		match('TIMES')
	elif currToken == 'OVER':
		match('OVER')
	else:
		parseError()
	_tabNum -= 1


	




if __name__ == '__main__':
	get_token = get_content()
	currToken = get_token[_tokenNum][1]
	#print(currToken)
	#currToken = get_token(_tokenNum)[1]
	Program() 
	#get_content()
