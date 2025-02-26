{
  description = "Angular 14 dev env with Node.js 18";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };


  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
  in {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = with pkgs; [
        nodejs_18
        nodePackages."@angular/cli"
        angular-language-server
        coreutils
        lsof
        typescript-language-server
      ];

      shellHook = ''
        echo "Node.js version: $(node -v)"
      '';
    };
  };
}

