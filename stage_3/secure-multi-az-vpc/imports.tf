import {
  to = aws_vpc.lab
  id = "vpc-02222810baaf794af"
}

import {
  to = aws_subnet.public_a
  id = "subnet-0c0ca2db62f743878"
}

import {
  to = aws_subnet.public_b
  id = "subnet-020eadfaf98561cd7"
}

import {
  to = aws_subnet.private_a
  id = "subnet-087ba18f8e885843b"
}

import {
  to = aws_subnet.private_b
  id = "subnet-054a8dd38c5612a3e"
}

import {
  to = aws_internet_gateway.lab
  id = "igw-069b8d2dc28162995"
}

import {
  to = aws_route_table.public
  id = "rtb-061154b6089f5720a"
}

import {
  to = aws_route_table_association.public_a
  id = "subnet-0c0ca2db62f743878/rtb-061154b6089f5720a"
}

import {
  to = aws_route_table_association.public_b
  id = "subnet-020eadfaf98561cd7/rtb-061154b6089f5720a"
}

import {
  to = aws_route_table.main
  id = "rtb-06d6b639bf6dedcb4"
}

import {
  to = aws_vpc_endpoint.s3
  id = "vpce-031522845c7fa7ada"
}

import {
  to = aws_security_group.web
  id = "sg-00f14e1dfa237b96a"
}
