A=[3,5,7]
B=[1,8]
C=[]
counter=0
while len(A)>0 and len(B)>0:
    if A[0] <= B[0]:
        C[counter]=A[0]
        A=A[1:]
        counter=counter+1
    else:
        C[counter]=B[0]
        B=B[1:]
        counter=counter+1

print(C)

