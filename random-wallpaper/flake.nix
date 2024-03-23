{
  description = "Script to set a random wallpaper";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };
  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    py3pkgs = pkgs.python3.pkgs;
  in
  {
    packages.${system}.default = pkgs.writers.writePython3Bin "random_wallpaper.py" 
    { 
      libraries = [py3pkgs.filelock];
    } "${builtins.readFile ./random_wallpaper.py}";
  };
  nixConfig = {};
}
