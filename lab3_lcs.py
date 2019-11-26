def lcs(s1,s2):
    m,n=len(s1),len(s2)
    chart = [[[] for i in range(n + 1)] for i in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if s1[i] == s2[j]:
                chart[i + 1][j + 1] = chart[i][j] + [s1[i]]
            elif len(chart[i][j + 1]) < len(chart[i + 1][j]):
                chart[i + 1][j + 1] = chart[i + 1][j]
            else:
                chart[i + 1][j + 1] = chart[i][1 + j]
    return chart[m][n]



s1=input('s1: ')
s2=input('s2: ')
print(''.join(lcs(s1,s2)))