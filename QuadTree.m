% View the block representation of quadtree decomposition.
close all;
%I = imread('liftingbody.png');
I = imread('C:\Users\LucasDESKPC\Documents\IndividualProject\croppedSpace.jpg');
I = imresize(I, 0.25);
[rows columns rgb] = size(I)
I = imrotate(I, -90);

% S is a sparse matrix 
S = qtdecomp(I,.6);

% Top left corner of box Box size in dimensions  
% (941,2047)     2
% Create empty array the size of the image ??? 
blocks = repmat(uint8(0),size(S));
% 
numQuadrants = 4;
vert = [ (1:(rows/numQuadrants):rows), rows ];
hori = [ (1:(columns/numQuadrants):columns), columns ];
xCord = [];
yCord = [];
average = []


% need to count number of blocks within cetain window. 
for dim = [512 256 128 64 32 16 8 4 2 1];    
  %  Look through s to find  
  numblocks = length(find(S==dim));
  
  if (numblocks > 0)        
    values = repmat(uint8(1),[dim dim numblocks]);
    values(2:dim,2:dim,:) = 0;
    
    % Blocks used to draw contours / edges. 
    blocks = qtsetblk(blocks,S,dim,values);
  end
end

numQuadrants = 4;
for curVer = 1:numQuadrants                 % Horiz
        for curHor = 1:numQuadrants
           quadrant = blocks(vert(curVer):vert(curVer + 1), hori(curHor):hori(curHor + 1) );
           total = sum(sum(quadrant));
           xCord = ((hori(curHor)+hori(curHor + 1))/2)
           yCord = ((vert(curVer)+vert(curVer + 1))/2)
           average = [ average; [total xCord yCord] ];
           % info = struct{ 'xPixel', hori(curHor) , 'yPixel', vert(curVer), 'sum', total}
        end
end

% for curVer = 1:numQuadrants                 % Horiz
%         for curHor = 1:numQuadrants
%            quadrant = blocks(vert(curVer):vert(curVer + 1), hori(curHor):hori(curHor + 1) );
%            total = sum(sum(quadrant));
%            average(curVer, curHor) = total
%            
%            if total> 1500
%            % take 2 highest points.     
%             xCord = [xCord, hori(curHor) ];
%             yCord = [yCord, vert(curVer)];
%             average(curVer, curHor) = 1;
%            end          
%         end
% end
%avg = reshape(average, [1, size(average, 1)^2 ] )
% max of each column. 
sortedAvg = sortrows(average, 1 )

sortedSize = size(sortedAvg,1 )
most = [ sortedAvg(sortedSize,1) sortedAvg(sortedSize, 2) sortedAvg(sortedSize, 3) ]
second = [ sortedAvg(sortedSize -1 ,1) sortedAvg(sortedSize -1, 2) sortedAvg(sortedSize -1, 3) ]


blocks(end,1:end) = 1;
blocks(1:end,end) = 1;

%imshow(I), figure, imshow(blocks,[])

%imshow(I);
shapeInserter = vision.ShapeInserter('Shape','Circles');

circles = [most(2) most(3) 30; second(2) second(3) 60];

% 
% for i = 1:size(xCord, 2)
%     cir = [xCord(i) yCord(i) 30];
%     circles = [circles; cir];
% end

circles = int32(circles);
circles
J = step(shapeInserter, I, circles);
imshow(J);

% 
% hold on 
% % x, y:    Center of the circle
%  % r:       Radius of the circle
% for i = 1:size(xCord)
%     x = xCord(i);
%     y = yCord(i);
%     r = 50;
%     theta = 0 : (2 * pi / 10000) : (2 * pi);
%     pline_x = r * cos(theta) + x;
%     pline_y = r * sin(theta) + y;
%     plot(pline_x, pline_y, '-');
% end
% hold off
