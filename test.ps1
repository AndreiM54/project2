echo "`tCPU Percentage: "
Get-WmiObject Win32_Processor | Select LoadPercentage | fl

echo "`tMore specifics regarding CPU : "

Get-Counter '\Process(*)\% Processor Time' `
    | Select-Object -ExpandProperty countersamples `
    | Select-Object -Property instancename, cookedvalue `
    | Sort-Object -Property cookedvalue -Descending | Select-Object -First 20 `
    | ft InstanceName,@{L='CPU';E={($_.Cookedvalue/100).toString('P')}} -AutoSize

echo "`tMemory information:"
Get-WmiObject win32_OperatingSystem |%{"`nTotal Physical Memory: {0}KB`nFree Physical Memory  : {1}KB ( {4}% )`nTotal Virtual Memory : {2}KB`nFree Virtual Memory : {3}KB ( {5}% )" -f $_.totalvisiblememorysize, $_.freephysicalmemory, $_.totalvirtualmemorysize, $_.freevirtualmemory, ($_.freephysicalmemory*100/$_.totalvisiblememorysize).toString('f2'), ($_.freevirtualmemory*100/$_.totalvirtualmemorysize).toString('f2')}


Read-Host -prompt "`n Press enter to exit."