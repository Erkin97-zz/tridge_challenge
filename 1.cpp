#include <bits/stdc++.h>

using namespace std;

vector <int> primes;

// todo: implement prime optimization
void find_primes() {
  bool f;
  for (int i = 2; i <= 100000; i++) {
    f = true;
    for (int k = 2; k <= sqrt(i); k++) {
      if (i % k == 0) {
        f = false;
        break;
      }
    }
    if (f) primes.push_back(i);
  }
}

int count_factors(int n) {
  int total_factor = 1, factor;

  for (int i = 0; n > 1; i++) {
    factor = 1;
    while (n % primes[i] == 0) {
      n /= primes[i];
      factor++;
    }
    total_factor *= factor;
  }

  return total_factor;
}

int main() {
  find_primes();
  int triangle_number = 1;

  for (int i = 2;; i++) {
    triangle_number += i; 
    if (count_factors(triangle_number) >= 500) {
      cout << triangle_number << endl;
      break;
    }
  }

  return 0;
}