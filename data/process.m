fileID = fopen('data');
C = textscan(fileID,'%s %s %s %s %s %s %s %s %s %s');
fclose(fileID);
names = cell(76,1);
data = cell(76,1);
for i=1:length(C)
    for j=1:length(C{i})
        if(isempty(str2num(C{i}{j}))&&~isempty(C{i}{j}))
            if(isempty(names{j}))
                names{j} = strtrim(C{i}{j});
            else
                names{j} = [names{j},' ',strtrim(C{i}{j})];
            end
        else
            temp=str2num(C{i}{j});
            if(isempty(data{j}))
                data{j} = temp;
            else
                data{j}=[data{j} temp];
            end
        end
    end
end
data_out=[];
inserted = 0;
for i=1:length(data)
    temp = data{i};
    if(length(temp)==6)
        data_out=[data_out; temp];
    else
        data_out=[data_out; [temp(1) temp(3:end)]];
        data_out=[data_out; [temp(2) temp(3:end)]];

        names = [names(1:i+inserted);names(i+inserted);names(i+inserted+1:end)];
        inserted= inserted+1;
    end
end
fid = fopen('data.csv','w');
for i=1:length(data_out)
    fprintf(fid,'%s',names{i});
    for j=1:6
        if(j==6)
            fprintf(fid,',%g\n',data_out(i,j));
        else
            fprintf(fid,',%g',data_out(i,j));
        end
    end
end
fclose(fid);

