import csv
def alias():
    input = []
    output = []

    with open('C:\\Users\\Lakshman\\Downloads\\input.csv', 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        fulllist = list(readCSV)
        for row in range(1, len(fulllist)):
            input.append(fulllist[row])
            print(input)
            a = fulllist[row][0]
            b = fulllist[row][1]
            output.append(a + b)
            output.append(a +'_'+  b)
            output.append(a +'-'+ b)
            output.append(a[0]+ b)
            output.append(a[0] +"_"+ b)
            output.append(a +"-" + b)
            output.append(a[0:3] + b)
            output.append(a[0:3] +"_"+ b)
            output.append(a[0:3] +"-"+ b)
            output.append(a[0]+b[0])
            output.append(a[0]+"_"+b[0])
            output.append(a[0]+"-"+b[0])
        f = open("C:\\Users\\Lakshman\\Documents\\testing.csv", "a")
        for i in output:
            f.write(i +'\n')


    print(output)

alias()
