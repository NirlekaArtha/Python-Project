   This python program takes your "message file" and insert/hide it into a PNG file a.k.a steganography.
This program could only process 4 channels PNG file at the moment. The program would take the png file 
that you had specified, open it, insert the message file into it, and then save back the png file into
the path that you had specified. the PNG would look the same (in human eyes) when get rendered by a 
media player or similiar program.

-Explanation 

   When a PNG get rendered, it will show us an image. This image is formed by several pixels, the ammount
of pixel of an image depends on it's dimension. These pixels are actually formed by several color channels,
the most common one is RGBA (Red, Green, Blue, and Alpha/transparency). We could edit these color channels
from the pixels that is in the image to contain our own "secret messages". but, if we edit these channels to much
and carelessly it may attract some attention due to a drastic changes of colors that had been made. 

   So how do i manage to hide it seemlessly? the trick is i hide the message in the last 2 digit of binary
in every single color channels. For example, i have a representation of message data and a pixel channel in binary.

*Before insertion*

10011011 --> the message

11111111 --> Red channel
00000000 --> Blue channel
11000000 --> Green channel
11110011 --> Alpha channel

I would then split it into 4 separate chunk (2 binary each chunk) and replace 2 digit of binary of each
color channel with the data chunks that i've prepared.

*After insertion*

11111110 --> Red channel
00000001 --> Blue channel
11000010 --> Green channel
11110011 --> Alpha channel

These channel/this pixel then stored into a buffer then get saved into a PNG file when the insertion have been
100% done.
