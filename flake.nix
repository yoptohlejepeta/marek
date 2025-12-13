{
  description = "LÖVE development environment with OpenGL support";

  inputs = {
    nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0";
    nixgl.url = "github:nix-community/nixGL";
  };

  outputs = { self, nixpkgs, nixgl, ... }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" ];
      forEachSupportedSystem = f:
        nixpkgs.lib.genAttrs supportedSystems (system:
          f {
            inherit system;
            pkgs = import nixpkgs {
              inherit system;
              config.allowUnfree = true;
              overlays = [ nixgl.overlays.default ];
            };
          });
    in {
      devShells = forEachSupportedSystem ({ pkgs, system }: {
        default = pkgs.mkShellNoCC {
          packages = [
            self.formatter.${system}
            pkgs.luajit
            pkgs.love
            pkgs.nixgl.auto.nixGLDefault
          ];

          env = { };

          shellHook = ''
            export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [ pkgs.libGL ]}:$LD_LIBRARY_PATH
          '';
        };
      });

      formatter = forEachSupportedSystem ({ pkgs, ... }: pkgs.nixfmt-rfc-style);
    };
}
