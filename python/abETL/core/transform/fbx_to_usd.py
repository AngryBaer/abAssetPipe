
import os
import hou
import abScan

from config import PipePaths


FBX_CONVERT = "fbx_to_usd_pipe.1.0.hdanc"
GEO_CONTAINER = "FBX_to_USD_pipe"


def install_hda(hda_name: str):
    """Installs the specified Houdini Digital Asset (HDA) from the HDAs directory."""
    hda_path = os.path.join(PipePaths.HDAS.value, hda_name)
    hou.hda.installFile(hda_path)
    return hda_path


def run_fbx_to_usd(input_file: os.PathLike = None, output_file: os.PathLike = None):
    """Runs the transformation process using the specified input and output files."""
    print(f"Running FBX to USD transformation on {os.path.basename(input_file)}")

    # Ensure the HDA is installed
    definition_file = install_hda(FBX_CONVERT)

    # Get the HDA node type
    hda_definition = hou.hda.definitionsInFile(definition_file)[0]

    # Create a geometry base node and a new node of the HDA type
    container_geo = hou.node("/obj").createNode("geo", node_name=GEO_CONTAINER)
    digital_asset = hou.node(f"/obj/{container_geo.name()}").createNode(hda_definition.nodeTypeName())

    digital_asset.parm("file").set(input_file)
    digital_asset.parm("lopoutput").set(output_file)
    digital_asset.parm("scale").set(0.01)
    digital_asset.parm("execute").pressButton()


if __name__ == "__main__":
    for input_fbx in abScan.iter_files(PipePaths.IN.value, abScan.make_pattern(".fbx")):
        output_usd = os.path.join(PipePaths.OUT.value, input_fbx.name.replace(".fbx", ".usd"))

        # Run the transformation
        run_fbx_to_usd(input_file=input_fbx.path, output_file=output_usd)
